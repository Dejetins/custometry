"""HTTP disconnect and task cancellation signal the actual columnar evaluator."""
import asyncio
from threading import Event

import pytest
from starlette.requests import Request

from custometry_api.analytics.filter_cancellation import cancellable_filter
from packages.contracts.analytics import AnalyticsFailure
from tests.integration.analytics.test_columnar_filters import setup as setup


def test_http_disconnect_cancels_real_evaluator_before_delivery(setup, monkeypatch):
    engine, access, query, _ = setup
    entered, ended = Event(), Event()
    original = engine._read
    def delayed(grant, cancel, deadline):
        entered.set()
        assert cancel.wait(1), 'HTTP disconnect did not reach evaluator'
        try:
            return original(grant, cancel, deadline)
        finally:
            ended.set()
    monkeypatch.setattr(engine, '_read', delayed)
    async def receive():
        return {'type': 'http.disconnect'}
    request = Request({'type':'http', 'method':'POST', 'path':'/filters/preview', 'headers':[]}, receive)
    async def check():
        with pytest.raises(AnalyticsFailure, match='FILTER_CANCELLED'):
            await cancellable_filter(request, lambda cancel: engine.execute(query, actor_id=access.grant.actor_id, cancel=cancel))
    asyncio.run(check())
    assert entered.is_set() and ended.is_set()


def test_handler_cancellation_waits_for_worker_exit():
    ended = Event()
    def operation(cancel):
        assert cancel.wait(1)
        ended.set()
        raise AnalyticsFailure('FILTER_CANCELLED')
    async def receive():
        await asyncio.sleep(10)
    request = Request({'type':'http', 'method':'POST', 'path':'/filters/preview', 'headers':[]}, receive)
    async def check():
        task = asyncio.create_task(cancellable_filter(request, operation))
        await asyncio.sleep(.03)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert ended.is_set()
    asyncio.run(check())

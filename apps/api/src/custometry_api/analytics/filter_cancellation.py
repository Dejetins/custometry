"""Propagate HTTP disconnect and handler cancellation to bounded CPU execution."""
import asyncio
from collections.abc import Callable
from contextlib import suppress
from threading import Event
from typing import TypeVar

from fastapi import Request

from packages.contracts.analytics import AnalyticsFailure

T = TypeVar('T')


async def cancellable_filter(request: Request, operation: Callable[[Event], T]) -> T:
    cancel = Event()
    task = asyncio.create_task(asyncio.to_thread(operation, cancel))
    try:
        while not task.done():
            await asyncio.wait({task}, timeout=0.025)
            if await request.is_disconnected():
                cancel.set()
        return await task
    finally:
        cancel.set()
        # A cancelled HTTP handler must not orphan CPU work or an unobserved error.
        with suppress(AnalyticsFailure, asyncio.CancelledError):
            await asyncio.shield(task)

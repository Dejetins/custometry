"""W39 real-PostgreSQL activity, replay retention and bounded maintenance proof."""

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from custometry_api.config import Settings
from packages.identity_access.application.service import IdentityService
from packages.identity_access.domain.policy import Actor
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository
from packages.identity_access.infrastructure.maintenance import IdentityMaintenance
from tests.integration.identity_access.conftest import connect, login, browser_headers


def session(client: TestClient, boot: dict[str, str], settings: Settings):
    response = login(
        client,
        email="owner@example.test",
        password="Owner-password-123!",
        workspace_id=boot["workspace_id"],
    )
    assert response.status_code == 200
    repo = PostgresIdentityRepository(lambda: connect(settings))
    service = IdentityService(repo, bootstrap_secret=None)
    actor = service.authenticate(response.cookies["custometry_access"])
    return response, repo, actor


def test_passive_reads_and_refresh_do_not_record_activity(
    client: TestClient, bootstrap_owner: dict[str, str], identity_settings: Settings
):
    response, _, actor = session(client, bootstrap_owner, identity_settings)
    with connect(identity_settings) as c:
        before = c.execute(
            "SELECT last_seen_at FROM identity_sessions WHERE id=%s", (actor.session_id,)
        ).fetchone()
    for _ in range(5):
        assert client.get("/identity/me").status_code == 200
    refreshed = client.post(
        "/identity/refresh", headers=browser_headers(response.json()["csrf_token"])
    )
    assert refreshed.status_code == 200
    with connect(identity_settings) as c:
        assert (
            c.execute(
                "SELECT last_seen_at FROM identity_sessions WHERE id=%s", (actor.session_id,)
            ).fetchone()
            == before
        )
        assert c.execute(
            "SELECT count(*) FROM identity_refresh_history WHERE session_id=%s", (actor.session_id,)
        ).fetchone() == (1,)


def test_interactive_activity_is_atomic_and_five_minute_bounded(
    client: TestClient, bootstrap_owner: dict[str, str], identity_settings: Settings
):
    _, repo, actor = session(client, bootstrap_owner, identity_settings)
    now = datetime.now(UTC) + timedelta(minutes=6)

    def record(_: int) -> bool:
        return repo.record_activity(actor, now)

    with ThreadPoolExecutor(max_workers=16) as pool:
        outcomes = list(pool.map(record, range(50)))
    assert sum(outcomes) == 1
    assert not repo.record_activity(actor, now + timedelta(minutes=4, seconds=59))
    assert repo.record_activity(actor, now + timedelta(minutes=5))
    assert actor.session_id is not None
    repo.revoke_session(actor, actor.session_id, now)
    assert not repo.record_activity(actor, now + timedelta(minutes=10))


def test_retention_preserves_replay_history_until_absolute_expiry_plus_seven_days(
    client: TestClient, bootstrap_owner: dict[str, str], identity_settings: Settings
):
    response, _, actor = session(client, bootstrap_owner, identity_settings)
    assert (
        client.post(
            "/identity/refresh", headers=browser_headers(response.json()["csrf_token"])
        ).status_code
        == 200
    )
    now = datetime.now(UTC)
    with connect(identity_settings) as c:
        c.execute(
            "UPDATE identity_sessions SET revoked_at=%s,absolute_expires_at=%s WHERE id=%s",
            (now - timedelta(days=30), now - timedelta(days=6), actor.session_id),
        )
        c.execute("UPDATE identity_maintenance_state SET last_completed_at=NULL WHERE id=1")
    job = IdentityMaintenance(lambda: connect(identity_settings))
    assert job.run(at=now)["sessions"] == 0
    with connect(identity_settings) as c:
        assert c.execute(
            "SELECT count(*) FROM identity_refresh_history WHERE session_id=%s", (actor.session_id,)
        ).fetchone() == (1,)
    assert job.run(at=now + timedelta(days=2))["sessions"] == 1
    with connect(identity_settings) as c:
        assert c.execute(
            "SELECT count(*) FROM identity_refresh_history WHERE session_id=%s", (actor.session_id,)
        ).fetchone() == (0,)


def test_cleanup_batch_and_category_boundaries(
    client: TestClient, bootstrap_owner: dict[str, str], identity_settings: Settings
):
    session(client, bootstrap_owner, identity_settings)
    now = datetime.now(UTC)
    with connect(identity_settings) as c:
        c.execute("UPDATE identity_audit_events SET occurred_at=%s", (now - timedelta(days=100),))
        c.execute("UPDATE identity_maintenance_state SET last_completed_at=NULL WHERE id=1")
        unrelated = c.execute(
            "SELECT count(*) FROM identity_audit_events WHERE action NOT LIKE 'session.%%' AND action NOT LIKE 'password.%%'"
        ).fetchone()
    result = IdentityMaintenance(lambda: connect(identity_settings)).run(
        at=now, batch_size=1, max_batches=1
    )
    assert result["events"] == 1
    assert (
        IdentityMaintenance(lambda: connect(identity_settings)).run(at=now)["status"] == "not_due"
    )
    with connect(identity_settings) as c:
        assert (
            c.execute(
                "SELECT count(*) FROM identity_audit_events WHERE action NOT LIKE 'session.%%' AND action NOT LIKE 'password.%%'"
            ).fetchone()
            == unrelated
        )


def test_revoke_is_a_committed_cross_connection_hint(
    client: TestClient, bootstrap_owner: dict[str, str], identity_settings: Settings
):
    response, _, _ = session(client, bootstrap_owner, identity_settings)
    with connect(identity_settings) as listener:
        listener.autocommit = True
        listener.execute("LISTEN custometry_identity_changed")
        assert (
            client.post(
                "/identity/logout", headers=browser_headers(response.json()["csrf_token"])
            ).status_code
            == 204
        )
        hints = list(listener.notifies(timeout=2, stop_after=1))
        assert len(hints) == 1 and hints[0].payload == "invalidate"


def test_interrupted_cleanup_rolls_back_and_retries(
    client: TestClient,
    bootstrap_owner: dict[str, str],
    identity_settings: Settings,
    monkeypatch: MonkeyPatch,
):
    response, _, actor = session(client, bootstrap_owner, identity_settings)
    assert (
        client.post(
            "/identity/refresh", headers=browser_headers(response.json()["csrf_token"])
        ).status_code
        == 200
    )
    now = datetime.now(UTC)
    with connect(identity_settings) as c:
        c.execute(
            "UPDATE identity_sessions SET absolute_expires_at=%s WHERE id=%s",
            (now - timedelta(days=8), actor.session_id),
        )
        c.execute("UPDATE identity_maintenance_state SET last_completed_at=NULL WHERE id=1")
    job = IdentityMaintenance(lambda: connect(identity_settings))
    import packages.identity_access.infrastructure.maintenance as module

    ticks = iter([0.0, 0.0, 0.0, 0.1, 99.0])
    with monkeypatch.context() as patch:
        patch.setattr(module, "monotonic", lambda: next(ticks))
        import pytest

        with pytest.raises(TimeoutError):
            job.run(at=now)
    with connect(identity_settings) as c:
        assert c.execute(
            "SELECT count(*) FROM identity_sessions WHERE id=%s", (actor.session_id,)
        ).fetchone() == (1,)
        assert c.execute(
            "SELECT count(*) FROM identity_refresh_history WHERE session_id=%s", (actor.session_id,)
        ).fetchone() == (1,)
        assert c.execute(
            "SELECT last_completed_at FROM identity_maintenance_state WHERE id=1"
        ).fetchone() == (None,)
    assert job.run(at=now)["sessions"] == 1


def test_fifty_sessions_controlled_hour_has_at_most_six_hundred_activity_updates(
    client: TestClient, bootstrap_owner: dict[str, str], identity_settings: Settings
):
    """Real SQL with a controlled application clock; not an elapsed-hour soak."""
    _, repo, first = session(client, bootstrap_owner, identity_settings)
    service = IdentityService(repo, bootstrap_secret=None)
    actors = [first]
    for i in range(49):
        tokens = service.login(
            email="owner@example.test",
            password="Owner-password-123!",
            workspace_id=first.workspace_id,
            device_label=f"W39 controlled activity {i}",
        )
        actors.append(service.authenticate(tokens.access_token))
    starts = datetime.now(UTC) + timedelta(minutes=6)
    updates = 0
    for minute in range(60):
        at = starts + timedelta(minutes=minute)

        def record(actor: Actor) -> bool:
            return repo.record_activity(actor, at)

        with ThreadPoolExecutor(max_workers=16) as pool:
            updates += sum(pool.map(record, actors))
    assert updates == 600


def test_request_projection_is_fresh_across_gets(
    client: TestClient, bootstrap_owner: dict[str, str], identity_settings: Settings
):
    from uuid import uuid4
    from packages.identity_access.infrastructure.resource_access import (
        PostgresResourceAccessRepository,
    )

    _, _, actor = session(client, bootstrap_owner, identity_settings)
    resource = uuid4()

    def source():
        return connect(identity_settings)

    ordinary = PostgresResourceAccessRepository(source)
    snapshot = PostgresResourceAccessRepository(source, request_snapshot=True)
    for action in ("view_snapshot", "edit"):
        expected = ordinary.resource_context(actor, "report", resource, action, actor.principal_id)
        assert (
            snapshot.resource_context(actor, "report", resource, action, actor.principal_id)
            == expected
        )
    # A subsequent protected request must see committed revocation, even though
    # the previous request legitimately reused its already-read projection.
    with source() as c:
        c.execute(
            "UPDATE identity_memberships SET status='suspended' WHERE workspace_id=%s AND principal_id=%s",
            (actor.workspace_id, actor.principal_id),
        )
    fresh = PostgresResourceAccessRepository(source, request_snapshot=True)
    assert (
        fresh.resource_context(actor, "report", resource, "view_snapshot", actor.principal_id)[
            "layers"
        ]["active_membership"]
        is False
    )


def test_read_pool_mode_restores_transactional_checkout(identity_settings: Settings):
    import psycopg
    import pytest
    from custometry_api.database import connection_factory

    reads = connection_factory(identity_settings, autocommit_reads=True)
    writes = connection_factory(identity_settings)
    with reads() as c:
        assert c.autocommit
        assert c.execute("SELECT 1").fetchone() == (1,)
        assert c.info.transaction_status == psycopg.pq.TransactionStatus.IDLE
        c.execute("CREATE TEMP TABLE w39_atomic_probe (value integer)")
        with pytest.raises(RuntimeError, match="rollback probe"):
            with c.transaction():
                c.execute("INSERT INTO w39_atomic_probe VALUES (1)")
                raise RuntimeError("rollback probe")
        assert c.execute("SELECT count(*) FROM w39_atomic_probe").fetchone() == (0,)
        c.execute("DROP TABLE w39_atomic_probe")
    with writes() as c:
        assert not c.autocommit
        c.execute("SELECT 1")
        assert c.info.transaction_status == psycopg.pq.TransactionStatus.INTRANS
    with reads() as c:
        assert c.autocommit
        assert c.info.transaction_status == psycopg.pq.TransactionStatus.IDLE

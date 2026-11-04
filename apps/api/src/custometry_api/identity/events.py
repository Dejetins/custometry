"""Bounded, lossy authorization hints backed by transactional PostgreSQL NOTIFY.

No payload contains a principal, token, resource or audit data. Reconnect is always
untrusted until the consumer repeats protected authorization. One listener per
worker fans out at most one pending hint to each of at most 256 connections.
"""

import asyncio
from datetime import UTC, datetime
from contextlib import suppress
import psycopg
from fastapi import Request
from fastapi.responses import StreamingResponse, JSONResponse
from custometry_api.config import Settings
from custometry_api.identity.http_auth import IdentityHTTPAdapter


class IdentityEvents:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.queues: set[asyncio.Queue[str]] = set()
        self.task: asyncio.Task[None] | None = None
        self.ready = asyncio.Event()

    def publish(self, value: str) -> None:
        for queue in tuple(self.queues):
            if queue.full():
                queue.get_nowait()
            queue.put_nowait(value)

    async def listen(self) -> None:
        s = self.settings
        try:
            async with await psycopg.AsyncConnection.connect(
                host=s.database_host,
                port=s.database_port,
                dbname=s.database_name,
                user=s.database_user,
                password=s.read_database_password(),
                connect_timeout=3,
                autocommit=True,
            ) as c:
                async with c.cursor() as cur:
                    await cur.execute(
                        "SELECT to_regprocedure('identity_notify_change()') IS NOT NULL"
                    )
                    row = await cur.fetchone()
                    if not row or not row[0]:
                        return
                    await cur.execute("LISTEN custometry_identity_changed")
                self.ready.set()
                async for _ in c.notifies():
                    self.publish("invalidate")
        except (psycopg.Error, OSError):
            pass  # No DSN, credentials or exception payload in diagnostics.
        finally:
            self.ready.clear()
            self.publish("disconnect")

    async def response(self, request: Request, auth: IdentityHTTPAdapter):
        # The listener must precede the handshake, closing the missed-event gap.
        if self.task is None or self.task.done():
            self.task = asyncio.create_task(self.listen())
        try:
            await asyncio.wait_for(self.ready.wait(), 3)
        except TimeoutError:
            return JSONResponse({"code": "AUTHORIZATION_CHANNEL_UNAVAILABLE"}, status_code=503)
        if len(self.queues) >= 256:
            return JSONResponse({"code": "AUTHORIZATION_CHANNEL_CAPACITY"}, status_code=503)
        queue: asyncio.Queue[str] = asyncio.Queue(maxsize=1)
        self.queues.add(queue)
        try:
            actor = await asyncio.to_thread(auth.authenticate, request)
            expires = await asyncio.to_thread(auth.service.session_deadline, actor)
            lifetime = max(0, min(600, (expires - datetime.now(UTC)).total_seconds() - 5))
        except BaseException:
            self.queues.discard(queue)
            raise

        async def stream():
            try:
                yield "event: connected\ndata: {}\n\n"
                deadline = asyncio.get_running_loop().time() + lifetime
                while not await request.is_disconnected():
                    if asyncio.get_running_loop().time() >= deadline:
                        yield "event: renew\ndata: {}\n\n"
                        return
                    try:
                        event = await asyncio.wait_for(
                            queue.get(),
                            max(0.01, min(15, deadline - asyncio.get_running_loop().time())),
                        )
                        yield f"event: {event}\ndata: {{}}\n\n"
                        if event == "disconnect":
                            return
                    except TimeoutError:
                        yield ": keepalive\n\n"
            finally:
                self.queues.discard(queue)

        return StreamingResponse(
            stream(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"},
        )

    async def close(self):
        if self.task:
            self.task.cancel()
            with suppress(asyncio.CancelledError):
                await self.task

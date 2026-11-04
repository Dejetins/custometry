"""Opt-in benchmark-only timing wrapper; no request values or credentials recorded."""
from contextvars import ContextVar
from contextlib import asynccontextmanager, contextmanager
import os
import gc
import sys
import cProfile
import pstats
from time import perf_counter, thread_time
import anyio.to_thread
import psycopg
from custometry_api.main import create_app as application

current = ContextVar('w39_timing', default=None)
original_execute = psycopg.Cursor.execute
original_thread = anyio.to_thread.run_sync
gc_started = {}
gc_elapsed = 0.0
gc_count = 0
gc_generations = [0.0, 0.0, 0.0]


def gc_observer(phase, info):
    global gc_elapsed, gc_count
    generation = info['generation']
    if phase == 'start':
        gc_started[generation] = perf_counter()
    elif generation in gc_started:
        duration = (perf_counter() - gc_started.pop(generation)) * 1000
        gc_elapsed += duration
        gc_generations[generation] += duration
        gc_count += 1


def execute(self, *args, **kwargs):
    timing = current.get()
    start = perf_counter()
    try:
        return original_execute(self, *args, **kwargs)
    finally:
        if timing is not None:
            timing['sql'] += (perf_counter() - start) * 1000
            timing['queries'] += 1


async def run_sync(function, *args, **kwargs):
    timing = current.get()
    queued = perf_counter()
    def invoke(*values):
        if timing is not None:
            timing['queue'] += (perf_counter() - queued) * 1000
        started_cpu = thread_time()
        profile = cProfile.Profile() if timing is not None and timing.get('profile') else None
        if profile:
            profile.enable()
        try:
            return function(*values)
        finally:
            if profile:
                profile.disable()
                with open(f'.runtime/w39/concurrent-profile-{os.getpid()}.txt', 'w') as output:
                    pstats.Stats(profile, stream=output).sort_stats('cumulative').print_stats(65)
            if timing is not None:
                timing['sync_cpu'] += (thread_time() - started_cpu) * 1000
    return await original_thread(invoke, *args, **kwargs)


class Timed:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)
        values = {'sql': 0., 'queue': 0., 'queries': 0, 'sync_cpu': 0., 'pool': 0.,
                  'profile': (b'x-w39-profile', b'1') in scope.get('headers', [])}
        token = current.set(values)
        start = perf_counter()
        initial_gc, initial_gc_count = gc_elapsed, gc_count
        initial_generations = gc_generations.copy()
        async def measured(message):
            if message['type'] == 'http.response.start':
                duration = (perf_counter() - start) * 1000
                timing = f'api;dur={duration:.3f}, thread_queue;dur={values["queue"]:.3f}, sync_cpu;dur={values["sync_cpu"]:.3f}, sql;dur={values["sql"]:.3f};desc="{values["queries"]} statements"'
                # Process-wide GC overlapping this request, not exclusive request
                # CPU: concurrent requests can observe the same collection.
                timing += f', overlapping_gc;dur={gc_elapsed-initial_gc:.3f};desc="{gc_count-initial_gc_count} process collections"'
                timing += ''.join(f', gc_gen{i};dur={gc_generations[i]-initial_generations[i]:.3f}' for i in range(3))
                timing += f', worker;desc="{os.getpid()}"'
                timing += f', pool_wait;dur={values["pool"]:.3f}'
                message['headers'] = list(message.get('headers', [])) + [(b'server-timing', timing.encode()), (b'x-w39-worker', str(os.getpid()).encode())]
            await send(message)
        try:
            await self.app(scope, receive, measured)
        finally:
            current.reset(token)


def create_app():
    try:
        from custometry_api import database
    except ImportError:
        database = None  # Frozen baseline has no pool adapter.
    if database is not None:
        original_factory = database.connection_factory
        def timed_factory(*args, **kwargs):
            source = original_factory(*args, **kwargs)
            @contextmanager
            def connect():
                start = perf_counter()
                with source() as connection:
                    timing = current.get()
                    if timing is not None:
                        timing['pool'] += (perf_counter() - start) * 1000
                    yield connection
            return connect
        database.connection_factory = timed_factory
        if os.environ.get('W39_POOL_SIZE'):
            from custometry_api import database
            original_pool = database.ConnectionPool
            class DiagnosticPool(original_pool):
                @classmethod
                def __class_getitem__(cls, item):
                    return cls
                def __init__(self, *args, **kwargs):
                    kwargs['max_size'] = int(os.environ['W39_POOL_SIZE'])
                    super().__init__(*args, **kwargs)
            database.ConnectionPool = DiagnosticPool
    gc.callbacks.append(gc_observer)
    if os.environ.get('W39_GC_THRESHOLD') and not os.environ.get('CUSTOMETRY_API_GC_ALLOCATION_THRESHOLD'):
        gc.set_threshold(int(os.environ['W39_GC_THRESHOLD']), 10, 10)
    if os.environ.get('W39_THREAD_SWITCH_SECONDS'):
        sys.setswitchinterval(float(os.environ['W39_THREAD_SWITCH_SECONDS']))
    psycopg.Cursor.execute = execute
    anyio.to_thread.run_sync = run_sync
    app = application()
    lifespan = app.router.lifespan_context
    @asynccontextmanager
    async def configured(instance):
        if os.environ.get('W39_THREAD_LIMIT') and not os.environ.get('CUSTOMETRY_API_SYNC_THREAD_LIMIT'):
            anyio.to_thread.current_default_thread_limiter().total_tokens = int(os.environ['W39_THREAD_LIMIT'])
        async with lifespan(instance):
            yield
    app.router.lifespan_context = configured
    return Timed(app)

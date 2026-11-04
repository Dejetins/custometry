"""Explicit process-local serving policy; unset values retain runtime defaults."""
from contextlib import contextmanager
import gc
from anyio.to_thread import current_default_thread_limiter
from custometry_api.config import Settings


@contextmanager
def serving_policy(settings: Settings):
    limiter = current_default_thread_limiter()
    prior_threads = limiter.total_tokens
    prior_gc = gc.get_threshold()
    if settings.api_sync_thread_limit is not None:
        limiter.total_tokens = settings.api_sync_thread_limit
    if settings.api_gc_allocation_threshold is not None:
        gc.set_threshold(settings.api_gc_allocation_threshold, *prior_gc[1:])
    try:
        yield
    finally:
        if settings.api_sync_thread_limit is not None:
            limiter.total_tokens = prior_threads
        if settings.api_gc_allocation_threshold is not None:
            gc.set_threshold(*prior_gc)

import asyncio
import gc
from anyio.to_thread import current_default_thread_limiter
from custometry_api.config import Settings
from custometry_api.runtime_policy import serving_policy


def test_explicit_policy_restores_runtime_after_failure():
    async def check():
        limiter = current_default_thread_limiter()
        prior_threads, prior_gc = limiter.total_tokens, gc.get_threshold()
        enabled = gc.isenabled()
        try:
            with serving_policy(Settings(api_sync_thread_limit=2, api_gc_allocation_threshold=1_000_000)):
                assert limiter.total_tokens == 2
                assert gc.get_threshold() == (1_000_000, *prior_gc[1:])
                assert gc.isenabled() == enabled
                raise RuntimeError("shutdown")
        except RuntimeError:
            pass
        assert limiter.total_tokens == prior_threads
        assert gc.get_threshold() == prior_gc
        with serving_policy(Settings()):
            assert limiter.total_tokens == prior_threads
            assert gc.get_threshold() == prior_gc
    asyncio.run(check())

import asyncio
from functools import wraps


def get_current_loop():
    return asyncio.get_event_loop()


def run_sync(res):
    """Run an async method in sync way
    CAUTION: Use only when in sync context
    """
    if asyncio.iscoroutine(res):
        loop = get_current_loop()
        return loop.run_until_complete(res)
    return res


def make_sync(fn):
    """
    turn an async function to sync function
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        return run_sync(res)

    return wrapper

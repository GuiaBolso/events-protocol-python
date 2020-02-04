import asyncio
from functools import wraps


def get_current_loop():
    return asyncio.get_event_loop()


def make_async(fn):
    """
    turns a sync function to async function using threads
    """
    from concurrent.futures import ThreadPoolExecutor
    import asyncio

    pool = ThreadPoolExecutor()

    @wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


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


class SyncMixin(object):
    """Make all public methods sync
    """

    def __new__(cls, *args, **kwargs):
        for method_name in dir(cls):
            if not method_name.startswith("_"):
                attr = getattr(cls, method_name)
                if callable(attr):
                    wrapped = make_sync(attr)
                    setattr(cls, method_name, wrapped)
                else:
                    setattr(cls, method_name, attr)
        return super().__new__(cls)

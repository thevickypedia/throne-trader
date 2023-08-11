from typing import Callable, TypeVar

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


def wraps(wrapper: Callable[P, T]):
    """An implementation of functools.wraps."""

    def decorator(func: Callable) -> Callable[P, T]:
        func.__doc__ = wrapper.__doc__
        return func

    return decorator

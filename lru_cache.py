from collections import OrderedDict
from typing import Any, Callable, Protocol, cast

class LRUCache:
    """ Simple Least Recently Used (LRU) cache. Stores key–value pairs up "
    "to a fixed capacity and automatically removes the least recently "
    "accessed item when the cache is full. """

    __slots__ = ("_max_size", "_lru", "_was_hit")

    _max_size: int | None
    _lru: OrderedDict[int, Any]
    _was_hit: bool

    def __init__(self, max_size: int | None = None) -> None:
        if max_size is not None:
            if not isinstance(max_size, int):
                raise TypeError(
                    "max_size must be an integer, but received "
                    f"{type(max_size).__name__}: {max_size}")

            if max_size <= 0:
                raise ValueError(
                    "max_size must be greater than 0, but received: "
                    f"{max_size}")

        self._max_size = max_size
        self._lru = OrderedDict[int, Any]()
        self._was_hit = False

    @property
    def max_size(self) -> int | None:
        return self._max_size

    @property
    def lru(self) -> OrderedDict[int, Any]:
        return self._lru

    @property
    def was_hit(self) -> bool:
        return self._was_hit

    def __len__(self) -> int:
        return len(self._lru)

    def __bool__(self) -> bool:
        return len(self._lru) > 0

    def get(self, *args: Any) -> Any:
        if not args:
            raise ValueError("get() requires at least one argument")

        hash_value: int = hash(args)

        if not self._lru or hash_value not in self._lru:
            self._was_hit = False

            return None

        last_hash_value: int = next(reversed(self._lru))

        if last_hash_value != hash_value:
            self._lru.move_to_end(hash_value)

        self._was_hit = True

        return self._lru[hash_value]

    def put(self, ret: Any, *args: Any) -> None:
        if not args:
            raise ValueError("put() requires at least one argument after 'ret'")

        hash_value: int = hash(args)

        if hash_value in self._lru:
            if next(reversed(self._lru)) != hash_value:
                self._lru.move_to_end(hash_value)

            return

        if self._max_size is not None \
           and len(self._lru) >= self._max_size:
            self._lru.popitem(last=False)

        self._lru[hash_value] = ret

class WrapperWithCache(Protocol):
    """Protocol used only to satisfy mypy for the lru_cache wrapper."""

    _cache: LRUCache

    def __call__(self, *args: Any) -> Any: ...

def lru_cache(max_size: int | None = None) \
    -> Callable[[Callable[..., Any]], WrapperWithCache]:
    """ LRU cache decorator similar to functools.lru_cache. """

    cache: LRUCache = LRUCache(max_size)

    def decorator(func: Callable[..., Any]) -> WrapperWithCache:
        def wrapper(*args: Any) -> Any:
            if not args:
                raise ValueError("args must contain at least one element")

            ret: Any | None = cache.get(*args)

            if ret is not None:
                return ret

            ret = func(*args)
            cache.put(ret, *args)

            return ret

        # Cast for mypy: tell the type checker that this wrapper has
        # a `_cache` attribute
        wrapped = cast(WrapperWithCache, wrapper)

        # Expose the cache for unit tests only (not intended for user code)
        wrapped._cache = cache

        return wrapped
    return decorator

from lru_cache import LRUCache, lru_cache
from typing import Any
import pytest

def test_lru_cache_collection_1() -> None:
    cache: LRUCache = LRUCache(1)

    assert cache.max_size == 1
    assert not cache.lru
    assert not cache.was_hit
    assert list(cache.lru.keys()) == []

    assert cache.get(1) is None
    assert cache.max_size == 1
    assert not cache.lru
    assert not cache.was_hit
    assert list(cache.lru.keys()) == []

    cache.put(2, 1)
    assert cache.max_size == 1
    assert len(cache.lru) == 1
    assert list(cache.lru.keys()) == \
        [hash((1,))]

    assert cache.get(1) == 2
    assert cache.max_size == 1
    assert len(cache.lru) == 1
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1,))]

    assert cache.get(2) is None
    assert cache.max_size == 1
    assert len(cache.lru) == 1
    assert not cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1,))]

    cache.put(4, 2)
    assert cache.max_size == 1
    assert len(cache.lru) == 1
    assert list(cache.lru.keys()) == \
        [hash((2,))]

    assert cache.get(2) == 4
    assert cache.max_size == 1
    assert len(cache.lru) == 1
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((2,))]

    assert cache.get(1) is None
    assert cache.max_size == 1
    assert len(cache.lru) == 1
    assert not cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((2,))]

def test_lru_cache_collection_2() -> None:
    cache: LRUCache = LRUCache(2)

    assert cache.max_size == 2
    assert not cache.lru
    assert not cache.was_hit
    assert list(cache.lru.keys()) == []

    assert cache.get(1, 'a') is None
    assert list(cache.lru.keys()) == []

    cache.put(2, 'a', 1)
    assert cache.max_size == 2
    assert len(cache.lru) == 1
    assert list(cache.lru.keys()) == \
        [hash(('a', 1))]

    assert cache.get('a', 1) == 2
    assert cache.max_size == 2
    assert len(cache.lru) == 1
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash(('a', 1))]

    cache.put(3, 'b', 2)
    assert cache.max_size == 2
    assert len(cache.lru) == 2
    assert list(cache.lru.keys()) == \
        [hash(('a', 1)),
         hash(('b', 2))]

    assert cache.get('a', 1) == 2
    assert cache.max_size == 2
    assert len(cache.lru) == 2
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash(('b', 2)),
         hash(('a', 1))]

    assert cache.get('b', 2) == 3
    assert cache.max_size == 2
    assert len(cache.lru) == 2
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash(('a', 1)), hash(('b', 2))]

    assert cache.get('a', 1) == 2
    assert cache.max_size == 2
    assert len(cache.lru) == 2
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash(('b', 2)),
         hash(('a', 1))]

    cache.put(4, 'c', 3)
    assert cache.max_size == 2
    assert len(cache.lru) == 2
    assert list(cache.lru.keys()) == \
        [hash(('a', 1)),
         hash(('c', 3))]

    assert cache.get('c', 3) == 4
    assert cache.max_size == 2
    assert len(cache.lru) == 2
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash(('a', 1)),
         hash(('c', 3))]

    assert cache.get('a', 1) == 2
    assert cache.max_size == 2
    assert len(cache.lru) == 2
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash(('c', 3)),
         hash(('a', 1))]

def test_lru_cache_collection_3() -> None:
    cache: LRUCache = LRUCache()

    assert cache.max_size is None
    assert not cache.lru
    assert not cache.was_hit
    assert list(cache.lru.keys()) == []

    assert cache.get(1, 2.0, True) is None
    assert cache.max_size is None
    assert not cache.lru
    assert not cache.was_hit
    assert list(cache.lru.keys()) == []

    cache.put('a', 1, 2.0, True)
    assert cache.max_size is None
    assert len(cache.lru) == 1
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, True))]

    assert cache.get(1, 2.0, True) == 'a'
    assert cache.max_size is None
    assert len(cache.lru) == 1
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, True))]

    assert cache.get(1, 2.0, False) is None
    assert cache.max_size is None
    assert len(cache.lru) == 1
    assert not cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, True))]

    cache.put('b', 1, 2.0, False)
    assert cache.max_size is None
    assert len(cache.lru) == 2
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, True)),
         hash((1, 2.0, False))]

    assert cache.get(1, 2.0, True) == 'a'
    assert cache.max_size is None
    assert len(cache.lru) == 2
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, False)),
         hash((1, 2.0, True))]

    assert cache.get(1, 2.0, False) == 'b'
    assert cache.max_size is None
    assert len(cache.lru) == 2
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, True)),
         hash((1, 2.0, False))]

    assert cache.get(1, 3.0, True) is None
    assert cache.max_size is None
    assert len(cache.lru) == 2
    assert not cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, True)),
         hash((1, 2.0, False))]

    cache.put('c', 1, 3.0, True)
    assert cache.max_size is None
    assert len(cache.lru) == 3
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, True)),
         hash((1, 2.0, False)),
         hash((1, 3.0, True))]

    assert cache.get(1, 3.0, True) == 'c'
    assert cache.max_size is None
    assert len(cache.lru) == 3
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, True)),
         hash((1, 2.0, False)),
         hash((1, 3.0, True))]

    assert cache.get(1, 2.0, False) == 'b'
    assert cache.max_size is None
    assert len(cache.lru) == 3
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, True)),
         hash((1, 3.0, True)),
         hash((1, 2.0, False))]

    assert cache.get(1, 2.0, True) == 'a'
    assert cache.max_size is None
    assert len(cache.lru) == 3
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 3.0, True)),
         hash((1, 2.0, False)),
         hash((1, 2.0, True))]

    assert cache.get(2, 2.0, False) is None
    assert cache.max_size is None
    assert len(cache.lru) == 3
    assert not cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 3.0, True)),
         hash((1, 2.0, False)),
         hash((1, 2.0, True))]

    cache.put('d', 2, 2.0, False)
    assert cache.max_size is None
    assert len(cache.lru) == 4
    assert list(cache.lru.keys()) == \
        [hash((1, 3.0, True)),
         hash((1, 2.0, False)),
         hash((1, 2.0, True)),
         hash((2, 2.0, False))]

    assert cache.get(2, 2.0, False) == 'd'
    assert cache.max_size is None
    assert len(cache.lru) == 4
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 3.0, True)),
         hash((1, 2.0, False)),
         hash((1, 2.0, True)),
         hash((2, 2.0, False))]

    assert cache.get(1, 3.0, True) == 'c'
    assert cache.max_size is None
    assert len(cache.lru) == 4
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, False)),
         hash((1, 2.0, True)),
         hash((2, 2.0, False)),
         hash((1, 3.0, True))]

    assert cache.get(1, 2.0, False) == 'b'
    assert cache.max_size is None
    assert len(cache.lru) == 4
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((1, 2.0, True)),
         hash((2, 2.0, False)),
         hash((1, 3.0, True)),
         hash((1, 2.0, False))]

    assert cache.get(1, 2.0, True) == 'a'
    assert cache.max_size is None
    assert len(cache.lru) == 4
    assert cache.was_hit
    assert list(cache.lru.keys()) == \
        [hash((2, 2.0, False)),
         hash((1, 3.0, True)),
         hash((1, 2.0, False)),
         hash((1, 2.0, True))]

def test_lru_cache_collection_4() -> None:
    with pytest.raises(TypeError):
        LRUCache(max_size='')

    with pytest.raises(ValueError):
        LRUCache(max_size=0)

    with pytest.raises(ValueError):
        LRUCache().get()

    with pytest.raises(ValueError):
        LRUCache().put(ret=0)


def test_lru_cache_decorator_1() -> None:
    @lru_cache(max_size=1)
    def square(n: int) -> int:
        return n * n

    assert square._cache.max_size == 1
    assert not square._cache.lru
    assert not square._cache.was_hit
    assert list(square._cache.lru.keys()) == []

    assert square._cache.get(2) is None
    assert square._cache.max_size == 1
    assert not square._cache.lru
    assert not square._cache.was_hit
    assert list(square._cache.lru.keys()) == []

    square(2)
    assert square._cache.max_size == 1
    assert len(square._cache.lru) == 1
    assert not square._cache.was_hit
    assert list(square._cache.lru.keys()) == \
        [hash((2,))]

    assert square._cache.get(2) == 4
    assert square._cache.max_size == 1
    assert len(square._cache.lru) == 1
    assert square._cache.was_hit
    assert list(square._cache.lru.keys()) == \
        [hash((2,))]

    assert square._cache.get(4) is None
    assert square._cache.max_size == 1
    assert len(square._cache.lru) == 1
    assert not square._cache.was_hit
    assert list(square._cache.lru.keys()) == \
        [hash((2,))]

    square(4)
    assert square._cache.max_size == 1
    assert len(square._cache.lru) == 1
    assert not square._cache.was_hit
    assert list(square._cache.lru.keys()) == \
        [hash((4,))]

    assert square._cache.get(4) == 16
    assert square._cache.max_size == 1
    assert len(square._cache.lru) == 1
    assert square._cache.was_hit
    assert list(square._cache.lru.keys()) == \
        [hash((4,))]

    assert square._cache.get(2) is None
    assert square._cache.max_size == 1
    assert len(square._cache.lru) == 1
    assert not square._cache.was_hit
    assert list(square._cache.lru.keys()) == \
        [hash((4,))]

def test_lru_cache_decorator_2() -> None:
    @lru_cache(max_size=2)
    def add(n: int, n2: int) -> int:
        return n + n2

    assert add._cache.max_size == 2
    assert not add._cache.lru
    assert not add._cache.was_hit
    assert list(add._cache.lru.keys()) == []

    assert add._cache.get(1, 1) is None
    assert add._cache.max_size == 2
    assert not add._cache.lru
    assert not add._cache.was_hit
    assert list(add._cache.lru.keys()) == []

    add(1, 1)
    assert add._cache.max_size == 2
    assert len(add._cache.lru) == 1
    assert not add._cache.was_hit
    assert list(add._cache.lru.keys()) == \
        [hash((1, 1))]

    assert add._cache.get(1, 1) == 2
    assert add._cache.max_size == 2
    assert len(add._cache.lru) == 1
    assert add._cache.was_hit
    assert list(add._cache.lru.keys()) == \
        [hash((1, 1))]

    assert add._cache.get(2, 2) is None
    assert add._cache.max_size == 2
    assert len(add._cache.lru) == 1
    assert not add._cache.was_hit
    assert list(add._cache.lru.keys()) == \
        [hash((1, 1))]

    add(2, 2)
    assert add._cache.max_size == 2
    assert len(add._cache.lru) == 2
    assert not add._cache.was_hit
    assert list(add._cache.lru.keys()) == \
        [hash((1, 1)),
         hash((2, 2))]

    assert add._cache.get(2, 2) == 4
    assert add._cache.max_size == 2
    assert len(add._cache.lru) == 2
    assert add._cache.was_hit
    assert list(add._cache.lru.keys()) == \
        [hash((1, 1)),
         hash((2, 2))]

    assert add._cache.get(1, 1) == 2
    assert add._cache.max_size == 2
    assert len(add._cache.lru) == 2
    assert add._cache.was_hit
    assert list(add._cache.lru.keys()) == \
        [hash((2, 2)),
         hash((1, 1))]

    assert add._cache.get(3, 3) == None
    assert add._cache.max_size == 2
    assert len(add._cache.lru) == 2
    assert not add._cache.was_hit
    assert list(add._cache.lru.keys()) == \
        [hash((2, 2)),
         hash((1, 1))]

    add(3, 3)
    assert add._cache.max_size == 2
    assert len(add._cache.lru) == 2
    assert not add._cache.was_hit
    assert list(add._cache.lru.keys()) == \
        [hash((1, 1)),
         hash((3, 3))]

    assert add._cache.get(1, 1) == 2
    assert add._cache.max_size == 2
    assert len(add._cache.lru) == 2
    assert add._cache.was_hit
    assert list(add._cache.lru.keys()) == \
        [hash((3, 3)),
         hash((1, 1))]

    assert add._cache.get(3, 3) == 6
    assert add._cache.max_size == 2
    assert len(add._cache.lru) == 2
    assert add._cache.was_hit
    assert list(add._cache.lru.keys()) == \
        [hash((1, 1)),
         hash((3, 3))]

    assert add._cache.get(2, 2) is None
    assert add._cache.max_size == 2
    assert len(add._cache.lru) == 2
    assert not add._cache.was_hit
    assert list(add._cache.lru.keys()) == \
        [hash((1, 1)),
         hash((3, 3))]

def test_lru_cache_decorator_3() -> None:
    @lru_cache(max_size=None)
    def args_len(*args: Any) -> int:
        return len(args)

    assert args_len._cache.max_size is None
    assert not args_len._cache.lru
    assert not args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == []

    assert args_len._cache.get(1) is None
    assert args_len._cache.max_size is None
    assert not args_len._cache.lru
    assert not args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == []

    args_len(1)
    assert args_len._cache.max_size is None
    assert len(args_len._cache.lru) == 1
    assert not args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == \
        [hash((1,))]

    assert args_len._cache.get(1) == 1
    assert args_len._cache.max_size is None
    assert len(args_len._cache.lru) == 1
    assert args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == \
        [hash((1,))]

    assert args_len._cache.get('a', 2.0, True) == None
    assert args_len._cache.max_size is None
    assert len(args_len._cache.lru) == 1
    assert not args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == \
        [hash((1,))]

    args_len('a', 2.0, True)
    assert args_len._cache.max_size is None
    assert len(args_len._cache.lru) == 2
    assert not args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == \
        [hash((1,)), hash(('a', 2.0, True))]

    assert args_len._cache.get('a', 2.0, True) == 3
    assert args_len._cache.max_size is None
    assert len(args_len._cache.lru) == 2
    assert args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == \
        [hash((1,)),
         hash(('a', 2.0, True))]

    assert args_len._cache.get(1) == 1
    assert args_len._cache.max_size is None
    assert len(args_len._cache.lru) == 2
    assert args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == \
        [hash(('a', 2.0, True)),
         hash((1,))]

    args_len(('my', 'string'), frozenset([]))
    assert args_len._cache.max_size is None
    assert len(args_len._cache.lru) == 3
    assert not args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == \
        [hash(('a', 2.0, True)),
         hash((1,)),
         hash((('my', 'string'), frozenset([])))]

    assert args_len._cache.get(('my', 'string'), frozenset([])) == 2
    assert args_len._cache.max_size is None
    assert len(args_len._cache.lru) == 3
    assert args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == \
        [hash(('a', 2.0, True)),
         hash((1,)),
         hash((('my', 'string'), frozenset([])))]

    assert args_len._cache.get('a', 2.0, True) == 3
    assert args_len._cache.max_size is None
    assert len(args_len._cache.lru) == 3
    assert args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == \
        [hash((1,)),
         hash((('my', 'string'), frozenset([]))),
         hash(('a', 2.0, True))]

    assert args_len._cache.get(1) == 1
    assert args_len._cache.max_size is None
    assert len(args_len._cache.lru) == 3
    assert args_len._cache.was_hit
    assert list(args_len._cache.lru.keys()) == \
        [hash((('my', 'string'), frozenset([]))),
         hash(('a', 2.0, True)),
         hash((1,))]

def test_lru_cache_decorator_4() -> None:
    with pytest.raises(ValueError):
        @lru_cache(max_size=None)
        def dummy() -> None:
            pass

        dummy()

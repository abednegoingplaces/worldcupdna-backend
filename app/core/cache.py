"""A tiny in-process TTL cache.

The football-data.org free tier allows only 10 requests/minute, so every
upstream call is cached for a short window. This is intentionally simple
(single-process, in-memory). For multi-instance deployments swap this for
Redis behind the same ``get``/``set`` interface.
"""
import threading
import time
from typing import Any, Callable, Optional

_store: dict[str, tuple[float, Any]] = {}
_lock = threading.Lock()


def get(key: str) -> Optional[Any]:
    with _lock:
        item = _store.get(key)
        if not item:
            return None
        expires_at, value = item
        if time.time() > expires_at:
            _store.pop(key, None)
            return None
        return value


def set(key: str, value: Any, ttl: int) -> None:
    with _lock:
        _store[key] = (time.time() + ttl, value)


def get_or_set(key: str, ttl: int, producer: Callable[[], Any]) -> Any:
    cached = get(key)
    if cached is not None:
        return cached
    value = producer()
    set(key, value, ttl)
    return value


def clear() -> None:
    with _lock:
        _store.clear()

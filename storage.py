from __future__ import annotations

from typing import Optional
from threading import Lock

from encoding import encode_base64, decode_base64  



# Storage functions for URL mappings
_storage: dict[str, str] = {}

# Monotonic counter used to generate new ids
_counter: int = 0

# Single lock to protect shared state
_lock = Lock()


def get_url(sid: str) -> str | Optional[str]:
    with _lock:
        return _storage.get(sid, None)


def set_url(sid: str, url: str) -> None:
    with _lock:
        _storage[sid] = url
    

def delete_id(sid: str) -> bool:
    with _lock:
        if sid in _storage:
            del _storage[sid]
            return True
        else:
            return False

def list_ids() -> list[str] | Optional[list[str]]:
    with _lock:
        return list(_storage.keys()) or None
    
def delete_ids() -> None:
    global _counter
    with _lock:
        _counter = 0
        _storage.clear()
   
def create_id(url: str) -> str:
    global _counter
    with _lock:
        _counter += 1
        sid = encode_base64(_counter)

        while sid in _storage:
            _counter += 1
            sid = encode_base64(_counter)

        _storage[sid] = url
        return sid
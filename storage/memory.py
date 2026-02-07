"""In-memory implementation of the storage."""

from __future__ import annotations
from threading import Lock
from typing import Optional
from utils.encoding import encode_base64
from storage.abstract_storage import AbstractStorage


class MemoryStorage(AbstractStorage):

    def __init__(self) -> None:
        self._storage: dict[str, str] = {}
        self._counter: int = 0
        self._lock = Lock()

    def get_url(self, id: str) -> str | Optional[str]:
        with self._lock:
            return self._storage.get(id, None)

    def set_url(self, id: str, url: str) -> None:
        with self._lock:
            self._storage[id] = url

    def delete_id(self, id: str) -> bool:
        with self._lock:
            if id in self._storage:
                del self._storage[id]
                return True
            return False

    def list_ids(self) -> list[str] | Optional[list[str]]:
        with self._lock:
            return list(self._storage.keys()) or None

    def delete_ids(self) -> None:
        with self._lock:
            self._counter = 0
            self._storage.clear()

    def create_id(self, url: str) -> str:
        with self._lock:
            self._counter += 1
            new_id = encode_base64(self._counter)
            while new_id in self._storage:
                self._counter += 1
                new_id = encode_base64(self._counter)
            self._storage[new_id] = url
            return new_id
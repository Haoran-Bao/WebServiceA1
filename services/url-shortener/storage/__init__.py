"""
Storage package: AbstractStorage and implementations.

Use DatabaseStorage or MemoryStorage based on the bonus flag in the config.

Returns DatabaseStorage if config.bonus is True, else MemoryStorage.
"""

from __future__ import annotations
from typing import Optional
from utils import config
from storage.abstract_storage import AbstractStorage
from storage.memory import MemoryStorage


def get_storage() -> AbstractStorage:
    if config.bonus:
        from storage.database import DatabaseStorage
        return DatabaseStorage()
    return MemoryStorage()


# Single storage instance
_storage: AbstractStorage = get_storage()


def get_url(id: str) -> str | Optional[str]:
    """Retrieve URL by ID."""
    return _storage.get_url(id)


def set_url(id: str, url: str) -> None:
    """Update URL for existing ID."""
    _storage.set_url(id, url)


def delete_id(id: str) -> bool:
    """Delete a ID. Returns True if deleted, False if not found."""
    return _storage.delete_id(id)


def list_ids() -> list[str] | Optional[list[str]]:
    """List all IDs."""
    return _storage.list_ids()


def delete_ids() -> None:
    """Delete all IDs and reset counter."""
    _storage.delete_ids()


def create_id(url: str) -> str:
    """Create a new ID for the given URL."""
    return _storage.create_id(url)
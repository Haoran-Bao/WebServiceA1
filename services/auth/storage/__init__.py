from .memory import MemoryStorage

_storage = MemoryStorage()


def create_user(username: str, password: str) -> bool:
    return _storage.create_user(username, password)


def update_password(username: str, old_password: str, new_password: str) -> bool:
    return _storage.update_password(username, old_password, new_password)


def verify_password(username: str, password: str) -> bool:
    return _storage.verify_password(username, password)

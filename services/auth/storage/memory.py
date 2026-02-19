from .abstract_storage import AbstractStorage


class MemoryStorage(AbstractStorage):
    def __init__(self) -> None:
        self._users: dict[str, str] = {}

    def create_user(self, username: str, password: str) -> bool:
        if username in self._users:
            return False
        self._users[username] = password
        return True

    def update_password(self, username: str, old_password: str, new_password: str) -> bool:
        if username not in self._users:
            return False
        if self._users[username] != old_password:
            return False
        self._users[username] = new_password
        return True

    def verify_password(self, username: str, password: str) -> bool:
        return self._users.get(username) == password

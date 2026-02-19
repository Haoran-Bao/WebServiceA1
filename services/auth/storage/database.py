"""Database(MongoDB) implementation of the storage."""

from threading import Lock
from pymongo import MongoClient
from storage.abstract_storage import AbstractStorage

from utils import config
from utils.password import hash_password, verify_password


class DatabaseStorage(AbstractStorage):
    def __init__(self) -> None:
        uri = f"mongodb://{config.mongodb_host}:{config.mongodb_port}/"
        client = MongoClient(uri)
        db = client[config.mongodb_database]
        users_name = config.mongodb_collections["users"]
        # {username: <username>, password: <hash>}
        self._users = db[users_name]
        self._lock = Lock()

    def create_user(self, username: str, password: str) -> bool:
        with self._lock:
            doc = self._users.find_one({"username": username})
            if doc is not None:
                return False
            self._users.insert_one(
                {"username": username, "password": hash_password(password)})
            return True

    def update_password(self, username: str, old_password: str, new_password: str) -> bool:
        with self._lock:
            if not self.verify_password(username, old_password):
                return False
            self._users.find_one_and_update(
                {"username": username},
                {"password": hash_password(new_password)}
            )
            return True

    def verify_password(self, username: str, password: str) -> bool:
        with self._lock:
            doc = self._users.find_one({"username": username})
            if doc is None:
                return False
            return verify_password(password, doc.get("password"))

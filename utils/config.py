"""Load configuration from config.json."""

from __future__ import annotations

import json
from pathlib import Path

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"

with open(_CONFIG_PATH, encoding="utf-8") as f:
    _config = json.load(f)

flask_host: str = _config["flask"]["host"]
flask_port: int = _config["flask"]["port"]
mongodb_port: int = _config["mongodb"]["port"]
mongodb_host: str = _config["mongodb"]["host"]
mongodb_database: str = _config["mongodb"]["database"]
mongodb_collections: dict[str, str] = _config["mongodb"]["collections"]
bonus: bool = _config["bonus"]

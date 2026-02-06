from __future__ import annotations

from typing import Optional
from threading import Lock

from encoding import encode_base64, decode_base64  

from pymongo import ReturnDocument
from db import mappings, counters


# Storage functions for URL mappings
#_storage: dict[str, str] = {}

# Monotonic counter used to generate new ids
#_counter: int = 0

# Single lock to protect shared state
_lock = Lock()


def get_url(sid: str) -> str | Optional[str]:
    with _lock:
        doc = mappings.find_one({"_id": sid}, {"url": 1})
        return None if doc is None else doc["url"]


def set_url(sid: str, url: str) -> None:
    with _lock:
        mappings.update_one({"_id": sid}, {"$set": {"url": url}}, upsert=False)
    

def delete_id(sid: str) -> bool:
    with _lock:
        res = mappings.delete_one({"_id": sid})
        return res.deleted_count == 1

def list_ids() -> list[str] | Optional[list[str]]:
    with _lock:
        ids = [d["_id"] for d in mappings.find({}, {"_id": 1})]
        return ids or None
    
def delete_ids() -> None:
    with _lock:
        mappings.delete_many({})
        # reset counter doc
        counters.update_one(
            {"_id": "url_id"},
            {"$set": {"seq": 0}},
            upsert=True,
        )
   
def create_id(url: str) -> str:
    with _lock:
        doc = counters.find_one_and_update(
            {"_id": "url_id"},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        seq = int(doc["seq"])
        sid = encode_base64(seq)
        
        # If sid somehow exists, keep incrementing
        # (shouldn't happen if encoding is deterministic and counter is monotonic)
        while mappings.find_one({"_id": sid}, {"_id": 1}) is not None:
            doc = counters.find_one_and_update(
                {"_id": "url_id"},
                {"$inc": {"seq": 1}},
                upsert=True,
                return_document=ReturnDocument.AFTER,
            )
            seq = int(doc["seq"])
            sid = encode_base64(seq)

        mappings.insert_one({"_id": sid, "url": url})
        return sid
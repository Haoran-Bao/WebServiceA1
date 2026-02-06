from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["url_shortener"]


# Collections
mappings = db["mappings"] # {_id: <sid>, url: <long_url>}
counters = db["counters"] # {_id: "url_id", value: <counter>}


# Assignment1 - Web Services and Cloud-Based Systems

URL shortener service built with Flask. It exposes a small REST API for creating, retrieving, updating, and deleting short URLs.

## Overview

The service stores URL-to-ID mappings **in memory**. Short IDs are generated with a monotonic counter and encoded using a URL-safe base64 alphabet (`A–Z`, `a–z`, `0–9`, `-`, `_`). Encoding and decoding helpers are present in `utils/encoding.py`.

## Requirements

- Python 3.10+ (tested with `python3`)
- Python packages: see `requirements.txt` (flask; `requests` for tests; `pymongo` for bonus)
- MongoDB running and reachable (e.g. locally at `mongodb://localhost:27017/`) (bonus) — required when `config.json` has `"bonus": true`

## Project Structure

- `app.py` — Flask app and routes
- `utils/encoding.py` — Base64-like ID encoding/decoding helpers.
- `utils/validation.py` — URL validation
- `utils/config.py` — Loads config values from `config.json`
- `storage/` — Storage layer: Package responsible for usage of in-memory or DB Storage based on config value
  - `storage/abstract_storage.py` — Abstract base class for storage
  - `storage/memory.py` — In-memory storage and ID generation (used by default)
  - `storage/database.py` — MongoDB storage (client and collection definitions) and ID generation (bonus)
- `.flaskenv` — Flask run settings (e.g. `FLASK_RUN_PORT=8000`)
- `config.json` — Configuration (MongoDB host/port/database/collections; bonus flag)
- `requirements.txt` — Python dependencies
- `test/test_1_marking_mk2.py` — Integration tests (service expected on port 8000)

## Configuration

- `**.flaskenv**` — Set `FLASK_RUN_PORT=8000` (or other port) for `flask run`.
- `**config.json**` holds:
  - `mongodb` (bonus) — `host`, `port`, `database`, `collections.mappings`, `collections.counters`; used when bonus is enabled
  - `bonus` (bonus) — when `true`, use MongoDB for storage; when `false`, use in-memory storage

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.

```bash
python -m venv .venv
# Windows:
. .venv/Scripts/activate
# macOS/Linux:
. .venv/bin/activate
pip install -r requirements.txt
```

## Run the service

Port is set in `.flaskenv` (e.g. 8000). Run with:

```bash
flask run
```

or `python app.py` (uses port 8000 by default).

## API

All endpoints are under `/`. Responses are JSON unless noted.

**1. `POST /**` — Create short URL

Request body:

```json
{ "value": "<long_url>" }
```

- 201: `{"id": "<short_id>"}`
- 400 on missing/invalid URL

**2. `GET /<id>**` — Resolve ID to URL

- 301: `{"value": "<long_url>"}`
- 404 if not found

**3. `PUT /<id>**` — Update URL mapping

Request body:

```json
{ "url": "<new_long_url>" }
```

- 200: `{"id": "<short_id>"}`
- 400 on invalid URL, 404 if not found

**4. `DELETE /<id>**` — Delete mapping

- 204 on success
- 404 if not found

**5. `GET /**` — List all short IDs

- 200:

```json
{"value": ["<id1>", "<id2>", ...]}
```

or

`{"value": null}` if empty

**6. `DELETE /**` — Delete all entries and reset counter

- Returns 404 (as expected by the provided tests)

## Testing

Start the service, then run:

```bash
python -s test/test_1_marking_mk2.py
```

---

## Bonus implementation

When the **bonus** option is enabled in config.json, the service uses **MongoDB** instead of in-memory storage. The same REST API and behaviour apply; only the storage backend changes.

### Enabling the bonus

In `config.json`, set:

```json
"bonus": true
```

With `bonus` true, the storage layer uses `storage/database.py` (**DatabaseStorage**) instead of `storage/memory.py` (MemoryStorage). The choice is made in `storage/__init__.py` via `get_storage()`.

### Configuration (bonus)

The `config.json` section `mongodb` is used only when `bonus` is true:

- `mongodb.host` — MongoDB host (default `localhost`)
- `mongodb.port` — MongoDB port (default `27017`)
- `mongodb.database` — Database name (e.g. `url_shortener`)
- `mongodb.collections.mappings` — Collection for ID → URL mappings
- `mongodb.collections.counters` — Collection for the monotonic counter

### Behaviour (bonus)

- **Mappings** are stored as documents `{ _id: "<id>", url: "<url>" }` in the mappings collection.
- **Counter** for generating new IDs is stored in the counters collection as a single document `{ _id: "url_id", seq: <number> }`. The value is incremented atomically; the number is then base64-encoded to produce the short ID.
- **Concurrency** is handled with a per-process lock in `DatabaseStorage`; the counter update uses MongoDB’s atomic `$inc`.
- `DELETE /` clears all documents in the mappings collection and resets the counter document to `seq: 0`.

All other endpoints, request/response formats, and test usage remain the same as in the base implementation.

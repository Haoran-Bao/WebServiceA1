# Assignment1 - Web Services and Cloud-Based Systems

URL shortener service and authentication service built with Flask. The URL shortener exposes a REST API for creating, retrieving, updating, and deleting short URLs, protected by JWT-based authentication.

## Overview

The URL shortener stores URL-to-ID mappings in memory by default. Short IDs are generated with a monotonic counter and encoded using a URL-safe base64 alphabet (`A-Z`, `a-z`, `0-9`, `-`, `_`). Encoding and decoding helpers are present in `services/url-shortener/utils/encoding.py`.

The authentication service issues JWTs and verifies them via a dedicated endpoint. JWTs are constructed manually (header + payload JSON, base64url encoding, and HS256 signature).

## Requirements

- Python 3.10+ (tested with `python3`)
- Python packages: see `requirements.txt` (flask; `requests` for tests; `pymongo` for bonus)
- MongoDB running and reachable (e.g. locally at `mongodb://localhost:27017/`) (bonus) required when `services/url-shortener/config.json` has `"bonus": true`

## Project Structure

- `services/auth/app.py` - Auth service Flask app and routes
- `services/auth/jwt.py` - Manual JWT construction and verification
- `services/auth/config.json` - Auth service configuration (JWT secret)
- `services/auth/storage/` - Auth storage abstraction and memory implementation
- `services/url-shortener/app.py` - URL shortener Flask app and routes
- `services/url-shortener/utils/` - URL shortener helpers (encoding, validation, frontend, auth client)
- `services/url-shortener/storage/` - URL shortener storage abstraction and implementations
- `services/url-shortener/config.json` - URL shortener configuration (MongoDB and bonus flag)
- `services/*/.flaskenv` - Flask run settings (ports)
- `requirements.txt` - Python dependencies
- `test/test_app.py` - Integration tests (services expected on ports 8000 and 8001)

## Configuration

- `services/auth/config.json` holds:
- `jwt.secret` - shared secret for HS256 signing and verification
- `services/url-shortener/config.json` holds:
- `mongodb` (bonus) - `host`, `port`, `database`, `collections.mappings`, `collections.counters`; used when bonus is enabled
- `bonus` (bonus) - when `true`, use MongoDB for storage; when `false`, use in-memory storage
- `AUTH_SERVICE_URL` (optional) - overrides auth service URL for the URL shortener (default `http://127.0.0.1:8001`)

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

## Run the services

Ports are set in each service `.flaskenv` (auth: 8001, url-shortener: 8000). Run each service from its folder with:

```bash
flask run
```

or `python app.py` in each service folder.

## API

URL shortener uses JWT auth on all endpoints except `GET /<id>`. The token is provided in the `Authorization` header.

**1. `POST /`** - Create short URL (auth required)

Request body:

```json
{ "value": "<long_url>" }
```

- 201: `{"id": "<short_id>"}`
- 400: `"error"`
- 403: `"forbidden"`

**2. `GET /<id>**` - Resolve ID to URL (public)

- 301: `{"value": "<long_url>"}`
- 404: `"error"`

**3. `PUT /<id>**` - Update URL mapping (auth required, owner-only)

Request body:

```json
{ "url": "<new_long_url>" }
```

- 200: `{"id": "<short_id>"}`
- 400: `"error"`
- 403: `"forbidden"`
- 404: `"error"`

**4. `DELETE /<id>**` - Delete mapping (auth required, owner-only)

- 204 on success
- 403: `"forbidden"`
- 404: `"error"`

**5. `GET /`** - List your short IDs (auth required)

- 200:

```json
{"value": ["<id1>", "<id2>", "..."]}
```

or

`{"value": null}` if empty

**6. `DELETE /`** - Delete all entries and reset counter (auth required)

- 403: `"forbidden"`
- 404: `"error"` (as expected by the provided tests)

**7. Auth service endpoints**

**`POST /users`** - Create user
- 201: `{"username": "<username>"}`
- 409: `"duplicate"`

**`PUT /users`** - Update password
- 200: `{"username": "<username>"}`
- 403: `"forbidden"`

**`POST /users/login`** - Login and receive JWT
- 201: `{"token": "<jwt>"}`
- 403: `"forbidden"`

**`POST /auth/verify`** - Verify JWT (used by URL shortener)
- 200: `{"payload": { ... }}`
- 403: `"forbidden"`

## Testing

Start both services, then run:

```bash
python -s test/test_app.py
```

---

## Bonus implementation

When the **bonus** option is enabled in `services/url-shortener/config.json`, the service uses **MongoDB** instead of in-memory storage. The same REST API and behaviour apply; only the storage backend changes.

### Enabling the bonus

In `services/url-shortener/config.json`, set:

```json
"bonus": true
```

With `bonus` true, the storage layer uses `storage/database.py` (**DatabaseStorage**) instead of `storage/memory.py` (MemoryStorage). The choice is made in `storage/__init__.py` via `get_storage()`.

### Configuration (bonus)

The `mongodb` section is used only when `bonus` is true:

- `mongodb.host` - MongoDB host (default `localhost`)
- `mongodb.port` - MongoDB port (default `27017`)
- `mongodb.database` - Database name (e.g. `url_shortener`)
- `mongodb.collections.mappings` - Collection for ID to URL mappings
- `mongodb.collections.counters` - Collection for the monotonic counter

### Behaviour (bonus)

- **Mappings** are stored as documents `{ _id: "<id>", url: "<url>", owner: "<username>" }` in the mappings collection.
- **Counter** for generating new IDs is stored in the counters collection as a single document `{ _id: "url_id", seq: <number> }`. The value is incremented atomically; the number is then base64-encoded to produce the short ID.
- **Concurrency** is handled with a per-process lock in `DatabaseStorage`; the counter update uses MongoDB's atomic `$inc`.
- `DELETE /` clears all documents in the mappings collection and resets the counter document to `seq: 0`.

### Web frontend

When the homepage (`GET /`) is requested with the `Accept: text/html` header,
a web frontend is returned instead of a JSON object with all URL IDs.
This frontend lets users shorten URLs, edit short URLs,
delete URLs and show all URLs.

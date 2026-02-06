# WebServiceA1

URL shortener service built with Flask and MongoDB. It exposes a small REST API for creating, retrieving, updating, and deleting short URLs.

**Overview**
This service stores URL mappings in MongoDB and generates short IDs using a monotonic counter encoded in a URL-safe base64 alphabet.

**Requirements**

- Python 3.10+ (tested with `python3`)
- MongoDB running locally on `mongodb://localhost:27017/`
- Python packages: `flask`, `pymongo`
- For tests: `requests`

**Project Structure**

- `app.py` Flask app and routes.
- `storage.py` MongoDB-backed storage and ID generation.
- `db.py` MongoDB client and collection definitions.
- `encoding.py` base64-like ID encoding/decoding helpers.
- `validation.py` URL validation.
- `test/test_1_marking_mk2.py` integration tests (expects service on port 8000).

**Setup**

1. Create and activate a virtual environment.
2. Install dependencies.

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install flask pymongo requests
```

**Run the Service**
The app runs on port 8000.

```bash
flask run -p 8000
```

**API**
All endpoints are rooted at `/`. Responses are JSON unless otherwise noted.

1. `POST /`

   - Body: `{"value": "<long_url>"}`
   - 201: `{"id": "<short_id>"}`
   - 400 on missing/invalid URL
2. `GET /<id>`

   - 301: `{"value": "<long_url>"}`
   - 404 if ID not found
3. `PUT /<id>`

   - Body: `{"url": "<new_long_url>"}`
   - 200: `{"id": "<short_id>"}`
   - 400 on invalid URL
   - 404 if ID not found
4. `DELETE /<id>`

   - 204 on success
   - 404 if ID not found
5. `GET /`

   - 200: `{"value": ["<id1>", "<id2>", ...]}` or `{"value": null}` if empty
6. `DELETE /`

   - Deletes all entries and resets the counter.
   - Returns 404 (as expected by the provided tests).

**Testing**
Start MongoDB and the service, then run:

```bash
python -m unittest test/test_1_marking_mk2.py
```

**Notes**

- The base64 alphabet in `encoding.py` is URL-safe: `A-Z a-z 0-9 - _`.
- The counter for new IDs is stored in `db.counters` as `{ _id: "url_id", seq: <int> }`.

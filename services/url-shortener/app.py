from flask import Flask, request, jsonify

from utils import validation, frontend
from utils.auth import verify_jwt
import storage

app = Flask(__name__)


@app.route('/<id>', methods=['GET'])
def get_with_id(id: str):
    url: str | None = storage.get_url(id)
    if url is None:
        return jsonify("error"), 404

    response = jsonify({"value": url})
    if frontend.requests_html(request.headers):
        response.headers.add_header("Location", url)
    return response, 301


@app.route('/<id>', methods=['PUT'])
def put_with_id(id: str):
    token = request.headers.get('Authorization')
    if verify_jwt(token) is None:
        return jsonify("forbidden"), 403
    # Also check if the user that updates the URL is the same user that created it
    url: str | None = storage.get_url(id)
    if url is None:
        return jsonify("error"), 404

    data: dict[str, str] = request.get_json(silent=True, force=True) or {}
    new_url: str | None = data.get('url')

    print(data, new_url)
    if new_url is None or not validation.is_valid_url(new_url):
        return jsonify("error"), 400

    storage.set_url(id, new_url.strip())

    return jsonify({"id": id}), 200


@app.route('/<id>', methods=['DELETE'])
def delete_with_id(id: str):
    token = request.headers.get('Authorization')
    if verify_jwt(token) is None:
        return jsonify("forbidden"), 403
    # Also check if the user that deletes the URL is the same user that created it
    if not storage.delete_id(id):
        return jsonify("error"), 404

    return '', 204


@app.route('/', methods=['GET'])
def get_all():
    if frontend.requests_html(request.headers):
        return frontend.respond_frontend()
    token = request.headers.get('Authorization')
    if verify_jwt(token) is None:
        return jsonify("forbidden"), 403
    return jsonify({"value": storage.list_ids()}), 200


@app.route('/', methods=['POST'])
def create_short_url():
    token = request.headers.get('Authorization')
    if verify_jwt(token) is None:
        return jsonify("forbidden"), 403
    # Also store the username next to the new URL
    data: dict[str, str] = request.get_json(silent=True, force=True) or {}
    url: str | None = data.get('value')

    if url is None or not validation.is_valid_url(url):
        return jsonify("error"), 400

    short_id = storage.create_id(url.strip())

    return jsonify({"id": short_id}), 201


@app.route('/', methods=['DELETE'])
def delete_all():
    token = request.headers.get('Authorization')
    if verify_jwt(token) is None:
        return jsonify("forbidden"), 403
    # By looking at the test, any user can call this for some reason
    storage.delete_ids()
    return jsonify("error"), 404

if __name__ == '__main__':
    app.run(port=8000, debug=True)

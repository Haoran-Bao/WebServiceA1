from flask import Flask, request, jsonify

import storage
import validation

app = Flask(__name__)

@app.route('/<id>', methods=['GET'])
def get_with_id(id):
    url: str | None = storage.get_url(id)
    if url is None:
        return jsonify("error"), 404

    return jsonify({"value": url}), 301


@app.route('/<id>', methods=['PUT'])
def put_with_id(id):
    url: str | None = storage.get_url(id)
    if url is None:
        return jsonify("Error - Not Found"), 404

    data: dict[str, str] = request.get_json(silent=True, force=True) or {}
    new_url: str | None = data.get('url')

    print(data, new_url)
    if new_url is None or not validation.is_valid_url(new_url):
        return jsonify("Error - Bad Request"), 400

    storage.set_url(id, new_url.strip())

    return jsonify({"id": id}), 200


@app.route('/<id>', methods=['DELETE'])
def delete_with_id(id):
    if not storage.delete_id(id):
        return jsonify("Error - Not Found"), 404

    return '', 204


@app.route('/', methods=['GET'])
def get_all():
    return jsonify({"value": storage.list_ids()}), 200


@app.route('/', methods=['POST'])
def create_short_url():
    data: dict[str, str] = request.get_json(silent=True, force=True) or {}
    url: str | None = data.get('value')

    if url is None or not validation.is_valid_url(url):
        return jsonify("Error - Bad Request"), 400

    short_id = storage.create_id(url.strip())

    return jsonify({"id": short_id}), 201


@app.route('/', methods=['DELETE'])
def delete_all():
    storage.delete_ids()
    return jsonify("Error"), 404

if __name__ == '__main__':
    app.run(port=8000, debug=True)

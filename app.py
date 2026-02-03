from flask import Flask, request, jsonify, redirect

import storage
import validation


app = Flask(__name__)

@app.route('/<id>', methods=['GET'])
def get_with_id(id):
    url: str | None = storage.get_url(id)
    if url is None:
        return jsonify("error"), 404

    return redirect(url, code=301)


@app.route('/<id>', methods=['PUT'])
def put_with_id(id):
    url: str | None = storage.get_url(id)
    if url is None:
        return jsonify("Error - Not Found"), 404

    data: dict[str, str] = request.get_json(silent=True) or {}
    url: str | None = data.get('url')

    if url is None or not validation.is_valid_url(url):
        return jsonify("Error - Bad Request"), 400

    storage.set_url(id, url.strip())

    return jsonify(id), 200


@app.route('/<id>', methods=['DELETE'])
def delete_with_id(id):
    if not storage.delete_id(id):
        return jsonify("Error - Not Found"), 404

    return '', 204


@app.route('/', methods=['GET'])
def get_all():
    return jsonify(storage.list_ids()), 200


@app.route('/', methods=['POST'])
def create_short_url():
    data: dict[str, str] = request.get_json(silent=True) or {}
    url: str | None = data.get('url')

    if url is None or not validation.is_valid_url(url):
        return jsonify("Error - Bad Request"), 400

    short_id = storage.create_id(url.strip())

    return jsonify(short_id), 201


@app.route('/', methods=['DELETE'])
def delete_all():
    return jsonify("Error"), 404

if __name__ == '__main__':
    app.run(debug=True)
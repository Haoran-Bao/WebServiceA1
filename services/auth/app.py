from flask import Flask, request, jsonify

from jwt import generate_jwt

app = Flask(__name__)


@app.route('/users', methods=['POST'])
def create_user():
    data: dict[str, str] = request.get_json(silent=True, force=True) or {}
    username = data['username']
    password = data['password']
    # ...
    # If this username already exists, return 409, "duplicate"
    return jsonify({'username': username}), 201


@app.route('/users', methods=['PUT'])
def update_password():
    data: dict[str, str] = request.get_json(silent=True, force=True) or {}
    username = data['username']
    old_password = data['old-password']
    new_password = data['new-password']
    # ...
    # If the old password is incorrect, return 403, "forbidden"
    return jsonify({'username': username}), 200


@app.route('/users/login', methods=['POST'])
def login():
    data: dict[str, str] = request.get_json(silent=True, force=True) or {}
    username = data['username']
    password = data['password']
    # ...
    # If the password is incorrect, return 403, "forbidden"
    token = generate_jwt(username)
    return jsonify({'token': token}), 201


if __name__ == '__main__':
    app.run(port=8001, debug=True)

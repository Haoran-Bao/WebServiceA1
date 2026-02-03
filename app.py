from flask import Flask

import storage
import validation


app = Flask(__name__)

@app.route('/<id>', methods=['GET'])
def get_with_id(id):
    pass


@app.route('/<id>', methods=['PUT'])
def put_with_id(id):
    pass


@app.route('/<id>', methods=['DELETE'])
def delete_with_id(id):
    pass


@app.route('/', methods=['GET'])
def get_all():
    pass


@app.route('/', methods=['POST'])
def create_short_url():
    pass

@app.route('/', methods=['DELETE'])
def delete_all():
    pass


if __name__ == '__main__':
    app.run(debug=True)
    
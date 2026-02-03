from flask import Flask

import storage
import validation


base64_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'


def int_to_base64(n: int):
    '''
    Convert an integer to a base 64 string.

    >>> int_to_base64(0)
    'A'
    >>> int_to_base64(1)
    'B'
    >>> int_to_base64(63)
    '_'
    >>> int_to_base64(64)
    'BA'
    >>> int_to_base64(100_000)
    'Yag'
    '''
    result = ''

    while n > 0:
        trailing_bits = n % 64
        result = base64_chars[trailing_bits] + result
        n = n // 64

    if result == '':
        return 'A'
    return result


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
    

from flask import Flask, send_file, send_from_directory

app = Flask(__name__)


@app.route('/<path:name>')
def serve(name):
    return send_from_directory('static', name)


@app.route('/')
def serve_index():
    return send_file('static/index.html')


if __name__ == '__main__':
    app.run(port=8002, debug=True)

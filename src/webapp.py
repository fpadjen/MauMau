import os
from flask import Flask, send_from_directory
from flask_sockets import Sockets

app = Flask(__name__, template_folder='../templates', static_folder='../static')
sockets = Sockets(app)


@app.route('/bower_components/<path:filename>')
def bower_components(filename):
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bower_components')), filename)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@sockets.route('/ws')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)

import os
from flask import Flask, send_from_directory
from flask_sockets import Sockets
import json
from threading import Thread
from bot import start, Interface

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static')
sockets = Sockets(app)


@app.route('/bower_components/<path:filename>')
def bower_components(filename):
    return send_from_directory(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..',
                'bower_components')
        ), filename)


@app.route('/')
def index():
    return app.send_static_file('index.html')


class WebsocketConnection(Thread, Interface):
    def __init__(self, ws):
        super(WebsocketConnection, self).__init__()
        self.ws = ws
        self.player = None

    def input_device(self, message=''):
        print 'input_adapter'
        data = {'player': self.player.to_dict(),
                'middle': self.player.current_middle}
        self.ws.send(json.dumps(data))
        if message:
            self.ws.send(message)
        return self.ws.receive()

    def output_device(self, message):
        print 'output_adapter'
        if isinstance(message, dict):
            print message
            self.ws.send(json.dumps(message))
        else:
            self.ws.send(message)


@sockets.route('/ws')
def echo_socket(ws):
    start(WebsocketConnection(ws))

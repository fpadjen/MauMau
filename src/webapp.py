import os
from flask import Flask, send_from_directory
from flask_sockets import Sockets
from maumau import Game
import random
import time
import json

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


class WebsocketConnection(object):
    def __init__(self, ws):
        self.ws = ws

    def input_adapter(self, message=''):
        if message:
            self.ws.send(message)
        return self.ws.receive()

    def output_adapter(self, message):
        if isinstance(message, dict):
            print message
            self.ws.send(json.dumps(message))
        else:
            self.ws.send(message)


@sockets.route('/ws')
def echo_socket(ws):
    wc = WebsocketConnection(ws)
    game = Game()
    game.add_player('bot1')
    game.add_player('bot2')
    game.add_player(
        'player',
        'h',
        output_device=wc.output_adapter,
        input_device=wc.input_adapter)
    game.state.setCurrentPlayer(
        random.randint(0, game.state.getNumTotalPlayers()))
    game.deal_cards_to_players(
        game.state.getNumTotalPlayers(),
        game.card_stack)
    game.start()

    while True:
        time.sleep(10)

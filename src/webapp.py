import os
from flask import Flask, send_from_directory
from flask_sockets import Sockets
from maumau import Game
import random
import time

app = Flask(__name__, template_folder='../templates', static_folder='../static')
sockets = Sockets(app)


@app.route('/bower_components/<path:filename>')
def bower_components(filename):
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bower_components')), filename)


@app.route('/')
def index():
    return app.send_static_file('index.html')


class WebsocketConnection(object):
    def __init__(self, ws):
        self.ws = ws

    def input_adapter(self, message):
        if message:
            self.ws.send(message)
        return self.ws.receive()


@sockets.route('/ws')
def echo_socket(ws):
    wc = WebsocketConnection(ws)
    game = Game(output=ws.send, input=wc.input_adapter)
    game.add_web_player()
    game.state.setCurrentPlayer(random.randint(0, game.state.getNumTotalPlayers()))
    game.deal_cards_to_players(game.state.getNumTotalPlayers(), game.card_stack)
    game.start()

    while True:
        time.sleep(10)

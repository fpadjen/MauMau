import os
from flask import Flask, send_from_directory
from flask_sockets import Sockets
from maumau import Game
import random
import time
import json
from threading import Thread
import redis

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


class WebsocketConnection(Thread):
    def __init__(self, ws, redis):
        super(WebsocketConnection, self).__init__()
        self.ws = ws
        self.redis = redis

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

    def run(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(['table'])
        for item in pubsub.listen():
            if item['type'] == 'subscribe':
                continue
            print item
            self.ws.send(item['data'])


@sockets.route('/ws')
def echo_socket(ws):
    REDIS_URL = os.environ.get('OPENREDIS_URL', 'redis://localhost:6379')
    wc = WebsocketConnection(ws, redis.from_url(REDIS_URL))
    wc.start()

    game = Game(redis.from_url(REDIS_URL))
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

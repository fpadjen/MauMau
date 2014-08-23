import os
from flask import Flask, send_from_directory
from flask_sockets import Sockets
import time
import json
from threading import Thread
import redis
from init_player import WaitForMessage
from random import randint
from player import Player
from deck import Deck
from time import sleep

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
    def __init__(self, ws):
        super(WebsocketConnection, self).__init__()
        self.ws = ws
        self.player = None

    def input_adapter(self, message=''):
        print 'input_adapter'
        data = {'player': self.player.to_dict(),
                'middle': self.player.current_middle}
        self.ws.send(json.dumps(data))
        if message:
            self.ws.send(message)
        return self.ws.receive()

    def output_adapter(self, message):
        print 'output_adapter'
        if isinstance(message, dict):
            print message
            self.ws.send(json.dumps(message))
        else:
            self.ws.send(message)


@sockets.route('/ws')
def echo_socket(ws):
    REDIS_URL = os.environ.get('OPENREDIS_URL', 'redis://localhost:6379')
    client = redis.from_url(REDIS_URL)

    wc = WebsocketConnection(ws)

    player = Player(
        'human{}'.format(randint(0, 1000)),
        'h',
        output_device=wc.output_adapter,
        input_device=wc.input_adapter)
    wc.player = player

    wait_for_message = WaitForMessage()
    wait_for_message.start()
    for _ in range(3):
        if not wait_for_message.waiting:
            break
        time.sleep(1)

    wait_for_message.active = False

    if wait_for_message.waiting:
        player.next_player = player.name
        player.start()
        time.sleep(1)
        client.publish(
            'table',
            json.dumps({
                'action': 'other',
                'middle': Deck.get_random_card(),
                'next': player.name}))
    else:
        player.next_player = wait_for_message.known_player
        client.publish(
            'table',
            json.dumps({
                'action': 'join',
                'player': player.name,
                'before': wait_for_message.known_player}))
        player.start()

    while True:
        if player.won:
            break
        sleep(5)

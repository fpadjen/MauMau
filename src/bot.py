from __future__ import print_function

import os
import redis
from player import Player
from random import randint
from threading import Thread
import time
import json
from deck import Deck
from time import sleep


class Interface(object):
    def output_device(self, message):
        raise NotImplemented

    def input_device(self):
        raise NotImplemented


class Bot(Interface):
    def __init__(self):
        super(Bot, self).__init__()
        self.player = None

    def output_device(self, message):
        print(message)

    def input_device(self):
        sleep(1)
        return 0


class WaitForMessage(Thread):
    def __init__(self):
        super(WaitForMessage, self).__init__()
        self.active = True
        self.waiting = True
        self.known_player = None

    def run(self):
        REDIS_URL = os.environ.get('OPENREDIS_URL', 'redis://localhost:6379')
        client = redis.from_url(REDIS_URL)
        pubsub = client.pubsub()
        pubsub.subscribe(['table'])

        for message in pubsub.listen():
            if self.active:
                print('WaitFor: {}'.format(message))
                if message['type'] == 'message':
                    data = json.loads(message['data'])
                    if data['action'] == 'quit':
                        continue
                    if 'player' in data:
                        self.known_player = data['player']
                        self.waiting = False
                        break
            else:
                break
        print('WaitFor exit')


def start(interface_class):
    REDIS_URL = os.environ.get('OPENREDIS_URL', 'redis://localhost:6379')
    client = redis.from_url(REDIS_URL)

    interface = interface_class()
    player = Player(
        'human{}'.format(randint(0, 1000)),
        'h',
        output_device=interface.output_device,
        input_device=interface.input_device)
    interface.player = player

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

    try:
        while True:
            if player.won:
                break
            sleep(5)
    except KeyboardInterrupt:
        client.publish(
            'table',
            json.dumps({
                'action': 'quit',
                'player': player.name,
                'next': player.next_player}))


def main():
    start(Bot)

if __name__ == '__main__':
    while True:
        main()

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


class Human(object):
    def __init__(self):
        self.player = None

    def output_device(self, message):
        print(message)

    def input_device(self):
        print(self.player.to_dict())
        return int(raw_input())


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


def main():
    REDIS_URL = os.environ.get('OPENREDIS_URL', 'redis://localhost:6379')
    client = redis.from_url(REDIS_URL)

    human = Human()
    player = Player(
        'human{}'.format(randint(0, 1000)),
        'h',
        output_device=human.output_device,
        input_device=human.input_device)
    human.player = player

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


if __name__ == '__main__':
    main()

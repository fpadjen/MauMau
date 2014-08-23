import os
import redis
from threading import Thread
import json
from deck import Deck


class Player(Thread):
    def __init__(self,
                 name=None,
                 output_device=None,
                 input_device=None):
        super(Player, self).__init__()
        self.name = name
        self.hand = [Deck.get_random_card() for _ in range(7)]
        self.playable_cards = []
        self.output_device = output_device
        self.input_device = input_device
        self.next_player = None
        REDIS_URL = os.environ.get('OPENREDIS_URL', 'redis://localhost:6379')
        self.client = redis.from_url(REDIS_URL)
        self.won = False
        self.current_middle = None

    def run(self):
        REDIS_URL = os.environ.get('OPENREDIS_URL', 'redis://localhost:6379')
        client = redis.from_url(REDIS_URL)
        pubsub = client.pubsub()
        pubsub.subscribe(['table'])

        for message in pubsub.listen():
            if message['type'] == 'subscribe':
                continue
            data = json.loads(message['data'])
            self.output_device(data)
            print('player: {} next: {} data: {}'
                  .format(self.name, self.next_player, data))
            if data['action'] == 'quit':
                if data['player'] == self.name:
                    break
                if data['player'] == self.next_player:
                    self.next_player = data['next']
                continue
            if data['action'] == 'won':
                if data['player'] == self.name:
                    break
                if data['player'] == self.next_player:
                    self.next_player = data['next']
                continue
            if data['action'] == 'join':
                if data['before'] == self.next_player:
                    self.next_player = data['player']
                continue
            self.current_middle = data['middle']
            if data['next'] == self.name:
                self.play(data)

    def publish(self, action, middle):
        self.client.publish(
            'table',
            json.dumps({
                'player': self.name,
                'action': action,
                'middle': middle,
                'next': self.next_player}))

    def play(self, data):
        if data['action'] != 'skip':
            if "seven" in data['middle']:
                self.draw_card()
                self.draw_card()
            elif "ace" in data['middle']:
                self.publish('skip', data['middle'])
                return

        self.init_playable_cards(data['middle'])

        if self.get_playable_card_count() == 0:
            self.draw_card()
            self.publish('drawcard', data['middle'])
            return

        card_to_play = self.choose_card()

        mau_state = self.check_mau()
        if mau_state == 0:
            self.client.publish('table', json.dumps({
                'action': 'won',
                'player': self.name,
                'next': self.next_player}))
            self.won = True

        self.publish('play', card_to_play)

    def to_dict(self):
        return {
            'name': self.name,
            'hand': self.hand,
            'playable_cards': self.playable_cards
        }

    def draw_card(self, card=None):
        if not card:
            card = Deck.get_random_card()
        self.hand.append(card)

    def get_playable_card_count(self):
        return len(self.playable_cards)

    def get_playable_cards(self):
        return self.playable_cards

    def init_playable_cards(self, middle):
        self.playable_cards = []
        if "jack" in middle:
            self.playable_cards = [i for i, _ in enumerate(self.hand)]
            return
        middle_value, middle_color = middle.split('_of_')
        for card in range(0, len(self.hand)):
            if (middle_color in self.hand[card]
                    or middle_value in self.hand[card]):
                self.playable_cards.append(card)

    def choose_card(self):
        return self.hand.pop(int(self.input_device()))

    def check_mau(self):
        if len(self.hand) == 1:
            # mau
            return 1
        elif len(self.hand) == 0:
            # maumau
            return 0
        else:
            return 1

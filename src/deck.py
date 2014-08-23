import random
from random import randint


class Deck:
    english_card_colors = ['spades', 'hearts', 'clubs', 'diamonds']
    english_card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10',
                           'jack', 'queen', 'king', 'ace']

    def __init__(self, name=None):
        self.deck = []
        self.middle_card = ''
        self.deck = self.create_deck()
        self.middle_card = str(self.deck.pop())

    def create_deck(self):
        for i in self.english_card_values:
            for j in self.english_card_colors:
                self.deck.append('{}_of_{}'.format(i, j))
                self.randomize_cardstack()
        # debug
        return self.deck

    def get_current_middle(self):
        return str(self.middle_card)

    def middle_to_stack(self):
        self.deck.append(self.middle_card)
        self.middle_card = ''

    def set_new_middle(self, card):
        self.middle_to_stack()
        self.middle_card = card

    def randomize_cardstack(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    @classmethod
    def get_random_card(cls):
        value = cls.english_card_values[
            randint(0, len(cls.english_card_values) - 1)]
        color = cls.english_card_colors[
            randint(0, len(cls.english_card_colors) - 1)]
        return '{}_of_{}'.format(value, color)

# -*- coding: utf-8 -*-

#
# This file is imported by maumau.py
# It contains the player class
#


class Player:

    def __init__(self, name=None, playerType=None):
        self.name = name
        self.hand = []
        self.playerType = playerType
        self.playable_cards = []

    def __repr__(self):
        return self.name

    def getCurrentPlayerName(self):
        return self.name

    def getCurrentPlayerType(self):
        return self.playerType

    def getPlayerlist(self):
        return self.playerList

    def draw_card(self, card):
        self.hand.append(card)

    def get_playable_card_count(self):
        return len(self.playable_cards)

    def get_playable_cards(self):
        return self.playable_cards

    def init_playable_cards(self, middle):
        middle_value, middle_color = middle.split(' of ')
        for card in range(0, len(self.hand)):
            if middle_color in self.hand[card] or middle_value in self.hand[card]:
                self.playable_cards.append(card)

    def get_card_to_play(self, number):
        self.check_mau()
        return self.hand.pop(self.playable_cards[number])

    def choose_card(self):
        # pick card to play, first from playable for now
        # build fancy algorithm here
        if len(self.playable_cards) == 0:
            print "I have no card i can play. Deal!"
            return 'Drinker of Drinks'
        else:
            self.check_mau()
            return self.hand.pop(self.playable_cards[0])

    def check_mau(self):
        if len(self.hand) == 1:
            print '%s: Last card! I call mau!' % (self.name.rstrip('\n'))
            return 1
        elif len(self.hand) == 0:
            print '%s I just placed my last card! maumau :D' % (self.name.rstrip('\n'))
            return 0
        else:
            return 1

    def get_card_count(self):
        return len(self.hand)

    def display_hand(self):
        print self.hand

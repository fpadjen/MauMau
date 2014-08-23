# -*- coding: utf-8 -*-

import random
import sys
from player import Player
from deck import Deck
from state import State


class Game(object):
    played_cards = []
    playerList = []
    card_stack = Deck()
    state = State()
    current_player = None

    def deal_cards_to_players(self, players, stack):
        for count in range(0, players):
            for _ in range(0, 6):
                # players[count].draw_card(stack.pop())
                self.playerList[count].draw_card(stack.deal_card())

    def add_player(
        self,
        name,
        player_type='b',
        output_device=None,
        input_device=None
    ):
        self.playerList.append(
            Player(
                name,
                player_type,
                output_device=output_device,
                input_device=input_device))
        self.state.incTotalPlayerCount()

    def check_special_cards(self):
        if "seven" in self.card_stack.get_current_middle():
            self.current_player.draw_card(self.card_stack.deal_card())
            self.current_player.draw_card(self.card_stack.deal_card())
        elif "jack" in self.card_stack.get_current_middle():
            pass
        elif "ace" in self.card_stack.get_current_middle():
            self.current_player.send({
                'action': 'skip',
                'middle': self.card_stack.get_current_middle(),
                'player': self.current_player.to_dict()})
            self.state.nextPlayer()
            self.state.setCurrentPlayer(
                self.state.getCurrentPlayer() % len(self.playerList))
            self.current_player = self.playerList[
                self.state.getCurrentPlayer()]
        else:
            pass

    def start(self):
        # main play loop starts here
        running = True
        while running:
            self.state.setCurrentPlayer(
                self.state.getCurrentPlayer() % len(self.playerList))
            self.current_player = self.playerList[
                self.state.getCurrentPlayer()]
            self.check_special_cards()

            self.current_player.init_playable_cards(
                self.card_stack.get_current_middle())

            if self.current_player.get_playable_card_count() == 0:
                self.card_stack.randomize_cardstack()
                self.current_player.draw_card(self.card_stack.deal_card())
                self.current_player.send({
                    'action': 'drawcard',
                    'middle': self.card_stack.get_current_middle(),
                    'player': self.current_player.to_dict()})
                continue

            self.current_player.send({
                'action': 'turn',
                'middle': self.card_stack.get_current_middle(),
                'player': self.current_player.to_dict()})

            card_to_play = self.current_player.choose_card()
            self.card_stack.set_new_middle(card_to_play)

            for player in self.playerList:
                player.send({
                    'action': 'other',
                    'middle': self.card_stack.get_current_middle()})

            mau_state = self.current_player.check_mau()
            if mau_state == 0:
                running = False
                for player in self.playerList:
                    player.send({
                        'action': 'won',
                        'winner': self.current_player.getCurrentPlayerName()})
                sys.exit(0)

            self.state.nextPlayer()

    def main(self):
        self.state.setCurrentPlayer(
            random.randint(0, self.state.getNumTotalPlayers()))
        self.deal_cards_to_players(
            self.state.getNumTotalPlayers(), self.card_stack)
        self.start()

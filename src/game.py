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

    def __init__(self, output, input_device):
        self.output = output
        self.input = input_device

    def deal_cards_to_players(self, players, stack):
        for count in range(0, players):
            for _ in range(0, 6):
                # players[count].draw_card(stack.pop())
                self.playerList[count].draw_card(stack.deal_card())

    def initPlayer(self):
        more_players = True
        while more_players:
            self.output("Enter player name please:")
            current_name = self.input()
            self.output("Is this a human or computer player?")
            self.output("Press h if the player is human, b if it is a bot.")
            player_type = self.input()

            if (player_type.lower() == "h") or player_type.lower() == "b":
                # create new object, name it by number starting with 0
                # add name to list playerList for access
                player = Player(current_name, player_type, output=self.output)
                self.playerList.append(player)
                self.output("debug: new player object created %r" % (player.getCurrentPlayerName()))
                self.state.incTotalPlayerCount()
            else:
                self.output("Please enter h or b to identify player type.")
                continue

            self.output("Add another player? (y/n)")
            if self.input() == "y":
                continue
            else:
                more_players = False

    def add_web_player(self):
        self.playerList.append(Player('player', 'h', output=self.output))
        self.state.incTotalPlayerCount()

        self.playerList.append(Player('bot1', 'b', output=self.output))
        self.state.incTotalPlayerCount()

        self.playerList.append(Player('bot2', 'b', output=self.output))
        self.state.incTotalPlayerCount()

        self.playerList.append(Player('bot3', 'b', output=self.output))
        self.state.incTotalPlayerCount()

    def check_special_cards(self):
        if "Seven" in self.card_stack.get_current_middle():
            self.output("You must draw 2 cards!")
            self.playerList[self.state.getCurrentPlayer()].draw_card(self.card_stack.deal_card())
            self.playerList[self.state.getCurrentPlayer()].draw_card(self.card_stack.deal_card())
        elif "Jack" in self.card_stack.get_current_middle():
            self.output("You can play any card you want!")
        elif "Ace" in self.card_stack.get_current_middle():
            self.output('You have bad luck, %s' % (self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerName()))
            self.state.nextPlayer()
            self.state.setCurrentPlayer(self.state.getCurrentPlayer() % len(self.playerList))
            self.output("%s, your turn." % (self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerName()))
        else:
            self.output("You can play a card from your hand or draw from the stack.")

    def main(self):
        self.initPlayer()
        self.state.setCurrentPlayer(random.randint(0, self.state.getNumTotalPlayers()))
        self.deal_cards_to_players(self.state.getNumTotalPlayers(), self.card_stack)
        self.start()

    def start(self):
        # main play loop starts here
        running = True
        while running:
            self.state.setCurrentPlayer(self.state.getCurrentPlayer() % len(self.playerList))
            self.output('%s, your turn to play!' % (self.playerList[self.state.getCurrentPlayer()]))
            self.output('The current card in the middle is the %s' % (self.card_stack.get_current_middle()))
            self.check_special_cards()
            self.output('You currently hold the following cards in your hand.')
            self.playerList[self.state.getCurrentPlayer()].display_hand()

            self.playerList[self.state.getCurrentPlayer()].init_playable_cards(self.card_stack.get_current_middle())
            self.output("debug: playable cards %r" % (self.playerList[self.state.getCurrentPlayer()].get_playable_cards()))
            if self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerType() == "h":
                # human player
                self.output("Middle card is %r" % (self.card_stack.get_current_middle()))
                if self.playerList[self.state.getCurrentPlayer()].get_playable_card_count() == 0:
                    self.card_stack.randomize_cardstack()
                    self.output("You do not have a card you can play. Drawing a card...")
                    self.playerList[self.state.getCurrentPlayer()].draw_card(self.card_stack.deal_card())
                else:
                    self.output("You can play the following cards:")
                    self.output("%r" % self.playerList[self.state.getCurrentPlayer()].get_playable_cards())
                    i = int(self.input("Enter number from above: "))
                    self.card_stack.set_new_middle(self.playerList[self.state.getCurrentPlayer()].get_card_to_play(i))
            elif self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerType() == "b":
                # bot player
                card_to_play = self.playerList[self.state.getCurrentPlayer()].choose_card()
                if self.playerList[self.state.getCurrentPlayer()].get_playable_card_count() == 0:
                    self.card_stack.randomize_cardstack()
                    self.playerList[self.state.getCurrentPlayer()].draw_card(self.card_stack.deal_card())
                else:
                    self.card_stack.set_new_middle(card_to_play)
                    self.output('%s says: I have played the %s' % (self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerName(), self.card_stack.get_current_middle()))

            mau_state = self.playerList[self.state.getCurrentPlayer()].check_mau()
            if mau_state == 0:
                running = False
                self.output('Player %s won!' % (self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerName()))
                sys.exit(0)

            self.state.nextPlayer()

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

    def deal_cards_to_players(self, players, stack):
        for count in range(0, players):
            for _ in range(0, 6):
                # players[count].draw_card(stack.pop())
                self.playerList[count].draw_card(stack.deal_card())
        # print 'debug: player 0 card info %r' % (players[0].get_card_count())

    def initPlayer(self):
        more_players = True
        while more_players:
            print "Enter player name please:"
            current_name = raw_input()
            print "Is this a human or computer player?"
            print "Press h if the player is human, b if it is a bot."
            player_type = raw_input()

            if (player_type.lower() == "h") or player_type.lower() == "b":
                # create new object, name it by number starting with 0
                # add name to list playerList for access
                playerID = Player(current_name, player_type)
                self.playerList.append(playerID)
                print "debug: new player object created %r" % (playerID.getCurrentPlayerName())
                self.state.incTotalPlayerCount()
            else:
                print "Please enter h or b to identify player type."
                continue

            print "Add another player? (y/n)"
            if raw_input() == "y":
                continue
            else:
                more_players = False

    def add_web_player(self):
        playerID = Player('player', 'h')
        self.playerList.append(playerID)
        self.state.incTotalPlayerCount()

        playerID = Player('bot1', 'b')
        self.playerList.append(playerID)
        self.state.incTotalPlayerCount()

        playerID = Player('bot2', 'b')
        self.playerList.append(playerID)
        self.state.incTotalPlayerCount()

        playerID = Player('bot3', 'b')
        self.playerList.append(playerID)
        self.state.incTotalPlayerCount()

    def check_special_cards(self):
        if "Seven" in self.card_stack.get_current_middle():
            print "You must draw 2 cards!"
            self.playerList[self.state.getCurrentPlayer()].draw_card(self.card_stack.deal_card())
            self.playerList[self.state.getCurrentPlayer()].draw_card(self.card_stack.deal_card())
        elif "Jack" in self.card_stack.get_current_middle():
            print "You can play any card you want!"
        elif "Ace" in self.card_stack.get_current_middle():
            print 'You have bad luck, %s' % (self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerName())
            self.state.nextPlayer()
            self.state.setCurrentPlayer(self.state.getCurrentPlayer() % len(self.playerList))
            print "%s, your turn." % (self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerName())
        else:
            print "You can play a card from your hand or draw from the stack."

    def main(self):
        self.initPlayer()
        self.state.setCurrentPlayer(random.randint(0, self.state.getNumTotalPlayers()))
        self.deal_cards_to_players(self.state.getNumTotalPlayers(), self.card_stack)

        # main play loop starts here
        running = True
        while running:
            self.state.setCurrentPlayer(self.state.getCurrentPlayer() % len(self.playerList))
            print '%s, your turn to play!' % (self.playerList[self.state.getCurrentPlayer()])
            print 'The current card in the middle is the %s' % (self.card_stack.get_current_middle())
            self.check_special_cards()
            print 'You currently hold the following cards in your hand.'
            self.playerList[self.state.getCurrentPlayer()].display_hand()

            self.playerList[self.state.getCurrentPlayer()].init_playable_cards(self.card_stack.get_current_middle())
            print "debug: playable cards %r" % (self.playerList[self.state.getCurrentPlayer()].get_playable_cards())
            if self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerType() == "h":
                # human player
                print "Middle card is %r" % (self.card_stack.get_current_middle())
                if self.playerList[self.state.getCurrentPlayer()].get_playable_card_count() == 0:
                    self.card_stack.randomize_cardstack()
                    print "You do not have a card you can play. Drawing a card..."
                    self.playerList[self.state.getCurrentPlayer()].draw_card(self.card_stack.deal_card())
                else:
                    print "You can play the following cards:"
                    print "%r" % self.playerList[self.state.getCurrentPlayer()].get_playable_cards()
                    i = int(raw_input("Enter number from above: "))
                    self.card_stack.set_new_middle(self.playerList[self.state.getCurrentPlayer()].get_card_to_play(i))
            elif self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerType() == "b":
                # bot player
                card_to_play = self.playerList[self.state.getCurrentPlayer()].choose_card()
                if self.playerList[self.state.getCurrentPlayer()].get_playable_card_count() == 0:
                    self.card_stack.randomize_cardstack()
                    self.playerList[self.state.getCurrentPlayer()].draw_card(self.card_stack.deal_card())
                else:
                    self.card_stack.set_new_middle(card_to_play)
                    print '%s says: I have played the %s' % (self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerName(), self.card_stack.get_current_middle())

            mau_state = self.playerList[self.state.getCurrentPlayer()].check_mau()
            if mau_state == 0:
                running = False
                print 'Player %s won!' % (self.playerList[self.state.getCurrentPlayer()].getCurrentPlayerName())
                sys.exit(0)

            self.state.nextPlayer()

#
# end main method
###

###
#
#
if __name__ == '__main__':
    game = Game()
    game.main()

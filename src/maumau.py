# -*- coding: utf-8 -*-

import random
import sys
from player import Player
from deck import Deck
from state import State

played_cards = []
playerList = []
card_stack = Deck()
state = State()


def deal_cards_to_players(players, stack):
    for count in range(0, players):
        for _ in range(0, 6):
            # players[count].draw_card(stack.pop())
            playerList[count].draw_card(stack.deal_card())
    # print 'debug: player 0 card info %r' % (players[0].get_card_count())


def initPlayer():
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
            playerID = state.getNumTotalPlayers()
            playerID = Player(current_name, player_type)
            playerList.append(playerID)
            print "debug: new player object created %r" % (playerID.getCurrentPlayerName())
            state.incTotalPlayerCount()
        else:
            print "Please enter h or b to identify player type."
            continue

        print "Add another player? (y/n)"
        if raw_input() == "y":
            continue
        else:
            more_players = False


def check_special_cards():
    if "Seven" in card_stack.get_current_middle():
        print "You must draw 2 cards!"
        playerList[state.getCurrentPlayer()].draw_card(card_stack.deal_card())
        playerList[state.getCurrentPlayer()].draw_card(card_stack.deal_card())
    elif "Jack" in card_stack.get_current_middle():
        print "You can play any card you want!"
    elif "Ace" in card_stack.get_current_middle():
        print 'You have bad luck. %s, your turn.' % (playerList[state.getCurrentPlayer()].getCurrentPlayerName())
        state.nextPlayer()
        state.setCurrentPlayer(state.getCurrentPlayer() % len(playerList))
    else:
        print "You can play a card from your hand or draw from the stack."


def main():

    initPlayer()
    state.setCurrentPlayer(random.randint(0, state.getNumTotalPlayers()))
    deal_cards_to_players(state.getNumTotalPlayers(), card_stack)

    # main play loop starts here
    running = True
    while running:
        state.setCurrentPlayer(state.getCurrentPlayer() % len(playerList))
        print '%s, your turn to play!' % (playerList[state.getCurrentPlayer()])
        print 'The current card in the middle is the %s' % (card_stack.get_current_middle())
        check_special_cards()
        print 'You currently hold the following cards in your hand.'
        playerList[state.getCurrentPlayer()].display_hand()

        playerList[state.getCurrentPlayer()].init_playable_cards(card_stack.get_current_middle())
        print "debug: playable cards %r" % (playerList[state.getCurrentPlayer()].get_playable_cards())
        if playerList[state.getCurrentPlayer()].getCurrentPlayerType() == "h":
            # human player
            print "Middle card is %r" % (card_stack.get_current_middle())
            if playerList[state.getCurrentPlayer()].get_playable_card_count() == 0:
                card_stack.randomize_cardstack()
                print "You do not have a card you can play. Drawing a card..."
                playerList[state.getCurrentPlayer()].draw_card(card_stack.deal_card())
            else:
                print "You can play the following cards:"
                print "%r" % playerList[state.getCurrentPlayer()].get_playable_cards()
                i = int(raw_input("Enter number from above: "))
                card_stack.set_new_middle(playerList[state.getCurrentPlayer()].get_card_to_play(i))
        elif playerList[state.getCurrentPlayer()].getCurrentPlayerType() == "b":
            # bot player
            card_to_play = playerList[state.getCurrentPlayer()].choose_card()
            if playerList[state.getCurrentPlayer()].get_playable_card_count() == 0:
                card_stack.randomize_cardstack()
                playerList[state.getCurrentPlayer()].draw_card(card_stack.deal_card())
            else:
                card_stack.set_new_middle(card_to_play)
                print '%s says: I have played the %s' % (playerList[state.getCurrentPlayer()].getCurrentPlayerName(), card_stack.get_current_middle())

        mau_state = playerList[state.getCurrentPlayer()].check_mau()
        if mau_state == 0:
            running = False
            print 'Player %s won!' % (playerList[state.getCurrentPlayer()].getCurrentPlayerName())
            sys.exit(0)

        state.nextPlayer()

#
# end main method
###

###
#
#
main()

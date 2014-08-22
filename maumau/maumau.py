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


def localize():
    print "Enter en for english cards, de for german cards"
    choice = raw_input()
    choice.lower()
    if 'de' in choice or 'en' in choice:
        return choice
    else:
        localize()



def deal_cards_to_players(players, stack):
    for count in range(0, players):
        for i in range(0, 6):
            #players[count].draw_card(stack.pop())
            player.getCurrentPlayer[count].draw_card(stack.deal_card())
    #print 'debug: player 0 card info %r' % (players[0].get_card_count())



def initPlayer():
    no_more_players = False
    while no_more_players != True:
        print "Enter player name please:"
        current_name = raw_input()
        print "Is this a human or computer player?"
        print "Press h if the player is human, b if it is a bot."
        player_type = raw_input()

        if (player_type.lower() == "h") or player_type.lower() == "b":
            # create new object, name it by number starting with 0, add name to list playerList for access
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
            no_more_players = True



def check_special_cards():
    if "Seven" in card_stack.get_current_middle():
        print "You must draw 2 cards!"
        player_list[player.getCurrentPlayer()].draw_card(card_stack.deal_card())
        player_list[player.getCurrentPlayer()].draw_card(card_stack.deal_card())
    elif "Jack" in card_stack.get_current_middle():
        print "You can play any card you want!"
    elif "Ace" in card_stack.get_current_middle():
        print 'You have bad luck. %s, your turn.' % (player_list[player.getCurrentPlayer()].name)
        player.nextPlayer()
        player.setCurrentPlayer(player.getCurrentPlayer() % len(player_list))
    else:
        print "You can play a card from your hand or draw from the stack."



def main():

    initPlayer()
    state.setCurrentPlayer(random.randint(0, state.getNumTotalPlayers()))

    print "debug: list of players %r" % playerList

    print "%s, you may start." % player.getCurrentPlayerName()

    deal_cards_to_players(player.getNumTotalPlayers(), card_stack)

    # main play loop starts here
    won = False
    while won != True:
        player.setCurrentPlayer(player.getCurrentPlayer() % len(player_list))
        print '%s, your turn to play!' % (player_list[player.getCurrentPlayer()].name.rstrip('\n'))
        print 'The current card in the middle is the %s' % (card_stack.get_current_middle())
        check_special_cards()
        print 'You currently hold the following cards in your hand.'
        player_list[player.getCurrentPlayer()].display_hand()
#        if human = True:
#            print 'Which card from 1 to %s do you want to play?' % (player_list[player.getCurrentPlayer()].get_card_count())
#            print 'Enter your choice.'
#            player_card = raw_input()

        card_to_play = player_list[player.getCurrentPlayer()].choose_card(card_stack.get_current_middle())
        if card_to_play == 'Drinker of Drinks':
            card_stack.randomize_cardstack()
            player_list[player.getCurrentPlayer()].draw_card(card_stack.deal_card())
        else:
            card_stack.set_new_middle(card_to_play)
            print '%s says: I have played the %s' % (player_list[player.getCurrentPlayer()].name.rstrip('\n'), card_stack.get_current_middle())

        mau_state = player_list[player.getCurrentPlayer()].check_mau()
        if mau_state == 0:
            won = True
            print 'Player %s won!' % (player_list[player.getCurrentPlayer()].name.rstrip('\n'))
            sys.exit(0)


        #print 'debug: current player number %r name %r' % (player.getCurrentPlayer(), player_list[player.getCurrentPlayer()].name)
        #print 'debug: current player hand size %r' % (player_list[player.getCurrentPlayer()].get_card_count())
        raw_input()
        player.nextPlayer()

#
# end main method
###

###
#
#
main()

# -*- coding: utf-8 -*-

from game import Game


def print_adapter(data):
    if isinstance(data, dict):
        if data['action'] == 'turn':
            print '{}, your turn to play!'.format(data['player'])
            print 'The current card in the middle is the {}'.format(data['middle'])
        elif data['action'] == 'skip':
            print 'You have bad luck, {}'.format(data['player'])
        else:
            print data
    else:
        print data


def input_adapter(message=''):
    return raw_input(message)

if __name__ == '__main__':
    game = Game(output=print_adapter, input_device=input_adapter)
    game.main()

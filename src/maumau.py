# -*- coding: utf-8 -*-

from game import Game


def print_adapter(data):
    print data


def input_adapter(message=''):
    return raw_input(message)

if __name__ == '__main__':
    game = Game(output=print_adapter, input=input_adapter)
    game.main()

# -*- coding: utf-8 -*-

from game import Game


def print_adapter(data):
    print data


if __name__ == '__main__':
    game = Game(output=print_adapter)
    game.main()

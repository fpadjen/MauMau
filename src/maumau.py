from __future__ import print_function

from game import Game
import os
import redis


def print_adapter(data):
    if isinstance(data, dict):
        if data['action'] == 'turn':
            print('{}, your turn to play!'.format(data['player']))
            print('The current card in the middle is the {}'
                  .format(data['middle']))
        elif data['action'] == 'skip':
            print('You have bad luck, {}'.format(data['player']))
        else:
            print(data)
    else:
        print(data)


def input_adapter(message=''):
    return raw_input(message)


def main():
    REDIS_URL = os.environ.get('OPENREDIS_URL', 'redis://localhost:6379')
    game = Game(redis.from_url(REDIS_URL))
    more_players = True
    while more_players:
        print("Enter player name please:")
        current_name = raw_input()

        while True:
            print("Press h if the player is human, b if it is a bot.")
            player_type = raw_input()
            print(player_type)
            if player_type.lower() == "h":
                game.add_player(
                    current_name,
                    player_type,
                    output_device=print_adapter,
                    input_device=input_adapter)
                break
            elif player_type.lower() == "b":
                game.add_player(current_name)
                break

        print("Add another player? (y/n)")
        if raw_input() == "y":
            continue
        else:
            more_players = False

    game.main()


if __name__ == '__main__':
    main()

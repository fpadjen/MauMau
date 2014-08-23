from __future__ import print_function

from init_player import start, Interface


class Human(Interface):
    def __init__(self):
        super(Human, self).__init__()
        self.player = None

    def output_device(self, message):
        print(message)

    def input_device(self):
        print(self.player.to_dict())
        return int(raw_input())


def main():
    start(Human)


if __name__ == '__main__':
    main()

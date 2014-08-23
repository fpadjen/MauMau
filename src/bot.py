from __future__ import print_function

from time import sleep
from init_player import start, Interface


class Bot(Interface):
    def __init__(self):
        super(Bot, self).__init__()
        self.player = None

    def output_device(self, message):
        print(message)

    def input_device(self):
        sleep(1)
        return 0


def main():
    start(Bot())

if __name__ == '__main__':
    while True:
        main()

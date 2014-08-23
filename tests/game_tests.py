from game import Game
import unittest


class GameTestCase(unittest.TestCase):

    def test_add_player(self):
        game = Game()
        list_length = len(game.playerList)
        game.add_player('player')
        self.assertEqual(list_length + 1, len(game.playerList))


if __name__ == '__main__':
    unittest.main()

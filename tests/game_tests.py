from game import Game
import unittest
from mock import Mock


class GameTestCase(unittest.TestCase):

    def test_add_player(self):
        redis = Mock()
        game = Game(redis)
        list_length = len(game.playerList)
        game.add_player('player')
        self.assertEqual(list_length + 1, len(game.playerList))


if __name__ == '__main__':
    unittest.main()

from state import State
import unittest


class StateTestCase(unittest.TestCase):

    def test_next_player(self):
        state = State()
        self.assertEqual(0, state.currentPlayer)
        state.nextPlayer()
        self.assertEqual(1, state.currentPlayer)

    def test_set_num_total_players(self):
        state = State()
        self.assertEqual(0, state.totalPlayerCount)
        state.setNumTotalPlayers(10)
        self.assertEqual(10, state.totalPlayerCount)

    def test_previous_player(self):
        state = State()
        self.assertEqual(0, state.currentPlayer)
        state.previousPlayer()
        self.assertEqual(-1, state.currentPlayer)

    def test_inc_total_player_count(self):
        state = State()
        self.assertEqual(0, state.totalPlayerCount)
        state.incTotalPlayerCount()
        self.assertEqual(1, state.totalPlayerCount)

    def test_get_num_total_players(self):
        state = State()
        state.incTotalPlayerCount()
        self.assertEqual(1, state.getNumTotalPlayers())

    def test_get_current_player(self):
        state = State()
        self.assertEqual(0, state.getCurrentPlayer())

    def test_set_current_player(self):
        state = State()
        state.setCurrentPlayer(2)
        self.assertEqual(2, state.currentPlayer)


if __name__ == '__main__':
    unittest.main()

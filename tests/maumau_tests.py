import maumau
import unittest
from mock import patch, Mock


class MauMauTestCase(unittest.TestCase):

    @patch('__builtin__.print')
    def test_print_adapter(self, _print):
        maumau.print_adapter('message')
        self.assertEqual(1, _print.call_count)

    @patch('__builtin__.print')
    def test_print_adapter_turn(self, _print):
        maumau.print_adapter({
            'action': 'turn',
            'player': 'player',
            'middle': 'middle'})
        self.assertEqual(2, _print.call_count)

    @patch('__builtin__.print')
    def test_print_adapter_skip(self, _print):
        maumau.print_adapter({
            'action': 'skip',
            'player': 'player',
            'middle': 'middle'})
        self.assertEqual(1, _print.call_count)

    @patch('__builtin__.print')
    def test_print_adapter_other(self, _print):
        maumau.print_adapter({
            'action': 'other',
            'player': 'player',
            'middle': 'middle'})
        self.assertEqual(1, _print.call_count)

    @patch('__builtin__.raw_input')
    def test_input_adapter(self, _input):
        maumau.input_adapter('message')
        self.assertTrue(_input.called)

    @patch('maumau.Game')
    @patch('__builtin__.raw_input')
    def test_main(self, _input, game_class):
        game = Mock()
        game_class.return_value = game
        _input.side_effect = ['bot', 'b', 'y', 'player', 'h', 'n']
        maumau.main()

if __name__ == '__main__':
    unittest.main()
import unittest
import bot
from mock import patch, Mock


class BotTestCase(unittest.TestCase):

    @patch('bot.start')
    def test_main(self, start):
        bot.main()
        self.assertTrue(start.called)

    @patch('__builtin__.print')
    def test_output_device(self, _print):
        b = bot.Bot()
        b.output_device('')
        self.assertTrue(_print.called)

    @patch('__builtin__.raw_input')
    def test_input_device(self, _input):
        b = bot.Bot()
        b.player = Mock()
        b.player.playable_cards = [0]
        self.assertEqual(0, b.input_device())


if __name__ == '__main__':
    unittest.main()

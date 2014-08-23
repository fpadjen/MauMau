import unittest
import human
from mock import patch, Mock


class HumanTestCase(unittest.TestCase):

    @patch('human.start')
    def test_main(self, start):
        human.main()
        self.assertTrue(start.called)

    @patch('__builtin__.print')
    def test_output_device(self, _print):
        h = human.Human()
        h.output_device('')
        self.assertTrue(_print.called)

    @patch('__builtin__.raw_input')
    def test_input_device(self, _input):
        h = human.Human()
        h.player = Mock()
        h.input_device()
        self.assertTrue(_input.called)


if __name__ == '__main__':
    unittest.main()

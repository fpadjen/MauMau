import unittest
import json
from mock import patch, Mock


class InitPlayerTestCase(unittest.TestCase):

    class Interfaces(unittest.TestCase):
        def output_device(self):
            self.assertRaises(NotImplemented)

        def input_device(self):
            self.assertRaises(NotImplemented)

    class WaitForMessage(unittest.TestCase):
        @patch('init_player.redis')
        def run(self, redis):
            pubsub = Mock()
            pubsub.listen.return_value = [
                {'type': 'subscribe'},
                {'type': 'message',
                 'data': json.dumps({
                     'action': 'quit',
                 })}]

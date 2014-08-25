import unittest
import json
from mock import patch, Mock, PropertyMock
from init_player import Interface, WaitForMessage, start, next_step, loop


class StartTestCase(unittest.TestCase):

    @patch('init_player.next_step')
    @patch('init_player.json')
    @patch('init_player.Player')
    @patch('init_player.sleep')
    @patch('init_player.WaitForMessage')
    @patch('init_player.redis')
    def test_start(self,
                   redis,
                   wait_for_message_class,
                   sleep,
                   player,
                   json,
                   next_step):
        interface = Mock()
        interface.input_device.return_value = 5
        wait_for_message = Mock()
        wait_for_message_class.return_value = wait_for_message
        type(wait_for_message).waiting = PropertyMock(
            side_effect=[True, False, True])
        start(interface)

    @patch('init_player.loop')
    @patch('init_player.json')
    def test_next_step_waiting(self, json, loop):
        player = Mock()
        client = Mock()
        waiting = True
        known_player = None
        next_step(player, client, waiting, known_player)

    @patch('init_player.loop')
    @patch('init_player.json')
    def test_next_step_not_waiting(self, json, loop):
        player = Mock()
        client = Mock()
        waiting = False
        known_player = None
        next_step(player, client, waiting, known_player)

    @patch('init_player.sleep')
    def test_loop(self, sleep):
        player = Mock()
        type(player).won = PropertyMock(side_effect=[False, True])
        client = Mock()
        loop(player, client)

    @patch('init_player.json')
    def test_loop_keyboard_interrupt(self, json):
        player = Mock()
        type(player).won = PropertyMock(side_effect=KeyboardInterrupt)
        client = Mock()
        loop(player, client)


class InterfaceTestCase(unittest.TestCase):

    def test_output_device(self):
        interface = Interface()
        self.assertRaises(Exception, interface.output_device, 'message')

    def test_input_device(self):
        interface = Interface()
        self.assertRaises(Exception, interface.input_device)


class WaitForMessageTestCase(unittest.TestCase):

    @patch('init_player.redis')
    def test_run_not_active(self, redis):
        wait_for_message = WaitForMessage()
        wait_for_message.active = False

        pubsub = Mock()
        pubsub.listen.return_value = [
            {'type': 'subscribe'}
        ]
        client = Mock()
        client.pubsub.return_value = pubsub
        redis.from_url.return_value = client
        wait_for_message.run()

        self.assertTrue(pubsub.subscribe)

    @patch('init_player.redis')
    def test_run_active(self, redis):
        wait_for_message = WaitForMessage()

        pubsub = Mock()
        pubsub.listen.return_value = [
            {'type': 'message',
             'data': json.dumps({'action': 'quit'})},
            {'type': 'message',
             'data': json.dumps({
                 'action': 'action',
                 'player': 'player'})},
        ]
        client = Mock()
        client.pubsub.return_value = pubsub
        redis.from_url.return_value = client
        wait_for_message.run()

        self.assertTrue(pubsub.subscribe)

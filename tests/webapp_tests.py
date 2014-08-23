import webapp
import unittest
from mock import Mock, patch
from webapp import WebsocketConnection


class WebappTestCase(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app.test_client()
        webapp.app.debug = True

    def tearDown(self):
        pass

    def test_get_bower(self):
        rv = self.app.get('/bower_components/bootstrap/dist/js/bootstrap.js')
        self.assertEqual(200, rv.status_code)

    def test_get_index(self):
        rv = self.app.get('/')
        self.assertEqual(200, rv.status_code)

    @patch('webapp.WaitForMessage')
    @patch('webapp.Player')
    @patch('webapp.WebsocketConnection')
    @patch('webapp.time')
    def test_echo_socket(self, time, ws, player, wait_for_message):
        time.sleep.side_effect = Exception
        ws = Mock()

        self.assertRaises(Exception, webapp.echo_socket, ws)


class WebsocketConnectionTestCase(unittest.TestCase):

    def test_input_adapter(self):
        ws = Mock()
        wc = WebsocketConnection(ws)
        player = Mock()
        player.to_dict.return_value = {}
        player.current_middle = 'middle'
        wc.player = player
        wc.input_adapter()
        self.assertEqual(1, ws.send.called)
        self.assertEqual(1, ws.receive.called)

    def test_input_adapter_with_message(self):
        ws = Mock()
        wc = WebsocketConnection(ws)
        player = Mock()
        player.to_dict.return_value = {}
        player.current_middle = 'middle'
        wc.player = player
        wc.input_adapter('message')
        self.assertEqual(1, ws.send.called)
        self.assertEqual(1, ws.receive.called)

    @patch('webapp.json')
    def test_output_adapter(self, json):
        ws = Mock()
        wc = WebsocketConnection(ws)
        wc.output_adapter('aa')
        self.assertEqual(1, ws.send.called)
        self.assertEqual(0, json.dumps.called)

    @patch('webapp.json')
    def test_output_adapter_dict(self, json):
        ws = Mock()
        wc = WebsocketConnection(ws)
        wc.output_adapter({'a': 'b'})
        self.assertEqual(1, ws.send.called)
        self.assertEqual(1, json.dumps.called)


if __name__ == '__main__':
    unittest.main()

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

    @patch('webapp.start')
    def test_echo_socket(self, start):
        ws = Mock()
        webapp.echo_socket(ws)
        self.assertTrue(start.called)


class WebsocketConnectionTestCase(unittest.TestCase):

    def test_input_device(self):
        ws = Mock()
        wc = WebsocketConnection(ws)
        player = Mock()
        player.to_dict.return_value = {}
        player.current_middle = 'middle'
        wc.player = player
        wc.input_device()
        self.assertEqual(1, ws.send.called)
        self.assertEqual(1, ws.receive.called)

    def test_input_device_with_message(self):
        ws = Mock()
        wc = WebsocketConnection(ws)
        player = Mock()
        player.to_dict.return_value = {}
        player.current_middle = 'middle'
        wc.player = player
        wc.input_device('message')
        self.assertEqual(1, ws.send.called)
        self.assertEqual(1, ws.receive.called)

    @patch('webapp.json')
    def test_output_device(self, json):
        ws = Mock()
        wc = WebsocketConnection(ws)
        wc.output_device('aa')
        self.assertEqual(1, ws.send.called)
        self.assertEqual(0, json.dumps.called)

    @patch('webapp.json')
    def test_output_device_dict(self, json):
        ws = Mock()
        wc = WebsocketConnection(ws)
        wc.output_device({'a': 'b'})
        self.assertEqual(1, ws.send.called)
        self.assertEqual(1, json.dumps.called)


if __name__ == '__main__':
    unittest.main()

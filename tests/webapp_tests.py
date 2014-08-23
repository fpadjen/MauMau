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

    @patch('webapp.WebsocketConnection')
    @patch('webapp.Game')
    @patch('webapp.time')
    def test_echo_socket(self, time, game_class, ws):
        game = Mock()
        game_class.return_value = game
        game.state.getNumTotalPlayers.return_value = 2

        time.sleep.side_effect = Exception
        ws = Mock()

        webapp.echo_socket(ws)
        self.assertTrue(game.start.called)


class WebsocketConnectionTestCase(unittest.TestCase):

    def test_input_adapter(self):
        ws = Mock()
        redis = Mock()
        wc = WebsocketConnection(ws, redis)
        wc.input_adapter()
        self.assertEqual(0, ws.send.called)
        self.assertEqual(1, ws.receive.called)

    def test_input_adapter_with_message(self):
        ws = Mock()
        redis = Mock()
        wc = WebsocketConnection(ws, redis)
        wc.input_adapter('message')
        self.assertEqual(1, ws.send.called)
        self.assertEqual(1, ws.receive.called)

    @patch('webapp.json')
    def test_output_adapter(self, json):
        ws = Mock()
        redis = Mock()
        wc = WebsocketConnection(ws, redis)
        wc.output_adapter('aa')
        self.assertEqual(1, ws.send.called)
        self.assertEqual(0, json.dumps.called)

    @patch('webapp.json')
    def test_output_adapter_dict(self, json):
        ws = Mock()
        redis = Mock()
        wc = WebsocketConnection(ws, redis)
        wc.output_adapter({'a': 'b'})
        self.assertEqual(1, ws.send.called)
        self.assertEqual(1, json.dumps.called)

    def test_run(self):
        ws = Mock()
        pubsub = Mock()
        pubsub.listen.return_value = [
            {'type': 'subscribe'},
            {'type': 'message', 'data': 'data'}]
        redis = Mock()
        redis.pubsub.return_value = pubsub
        wc = WebsocketConnection(ws, redis)
        wc.run()

if __name__ == '__main__':
    unittest.main()

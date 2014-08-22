import webapp
import unittest
from mock import Mock


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

    def test_echo_socket(self):
        ws = Mock()
        ws.send.side_effect = Exception
        self.assertRaises(Exception, webapp.echo_socket, ws)

if __name__ == '__main__':
    unittest.main()

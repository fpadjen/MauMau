from player import Player
import unittest
from mock import Mock, patch
import json


class PlayerTestCase(unittest.TestCase):

    @patch('player.redis')
    @patch('player.os')
    def test_run(self, os, redis):
        player = Player('player')
        player.play = Mock()
        pubsub = Mock()
        pubsub.listen.return_value = [
            {'type': 'subscribe'},
            {'type': 'message',
             'data': json.dumps({
                 'action': 'quit',
                 'player': 'name'})},
            {'type': 'message',
             'data': json.dumps({
                 'action': 'won',
                 'player': 'name'})},
            {'type': 'message',
             'data': json.dumps({
                 'action': 'join',
                 'before': 'name'})},
            {'type': 'message',
             'data': json.dumps({
                 'action': 'skip',
                 'next': player.name})},
            {'type': 'message',
             'data': json.dumps({
                 'action': 'won',
                 'player': player.name})},
        ]
        client = Mock()
        client.pubsub.return_value = pubsub
        redis.from_url.return_value = client

        player.run()
        self.assertTrue(client.pubsub.called)
        self.assertTrue(pubsub.subscribe.called)

    @patch('player.redis')
    @patch('player.os')
    def test_run_quit_self(self, os, redis):
        player = Player('player')
        player.play = Mock()
        pubsub = Mock()
        pubsub.listen.return_value = [
            {'type': 'message',
             'data': json.dumps({
                 'action': 'quit',
                 'player': player.name})},
        ]
        client = Mock()
        client.pubsub.return_value = pubsub
        redis.from_url.return_value = client

        player.run()
        self.assertTrue(client.pubsub.called)
        self.assertTrue(pubsub.subscribe.called)

    @patch('player.redis')
    @patch('player.os')
    def test_run_quit_other(self, os, redis):
        player = Player('player')
        player.play = Mock()
        pubsub = Mock()
        pubsub.listen.return_value = [
            {'type': 'message',
             'data': json.dumps({
                 'action': 'quit',
                 'player': 'other'})},
        ]
        client = Mock()
        client.pubsub.return_value = pubsub
        redis.from_url.return_value = client

        player.run()
        self.assertTrue(client.pubsub.called)
        self.assertTrue(pubsub.subscribe.called)

    @patch('player.redis')
    @patch('player.os')
    def test_run_won_self_next(self, os, redis):
        player = Player('player')
        player.next_player = 'winner'
        player.play = Mock()
        pubsub = Mock()
        pubsub.listen.return_value = [
            {'type': 'message',
             'data': json.dumps({
                 'action': 'won',
                 'player': 'winner',
                 'next': 'next'})},
            {'type': 'message',
             'data': json.dumps({
                 'action': 'won',
                 'player': 'looser',
                 'next': 'next'})},
        ]
        client = Mock()
        client.pubsub.return_value = pubsub
        redis.from_url.return_value = client

        player.run()
        self.assertTrue(client.pubsub.called)
        self.assertTrue(pubsub.subscribe.called)

    @patch('player.redis')
    @patch('player.os')
    def test_run_won_join_self_next(self, os, redis):
        player = Player('player')
        player.next_player = 'winner'
        player.play = Mock()
        pubsub = Mock()
        pubsub.listen.return_value = [
            {'type': 'message',
             'data': json.dumps({
                 'action': 'join',
                 'before': player.next_player,
                 'player': 'player'})},
        ]
        client = Mock()
        client.pubsub.return_value = pubsub
        redis.from_url.return_value = client

        player.run()
        self.assertTrue(client.pubsub.called)
        self.assertTrue(pubsub.subscribe.called)

    def test_to_dict(self):
        player = Player('player')
        data = player.to_dict()
        self.assertEqual('player', data['name'])
        self.assertEqual([], data['hand'])
        self.assertEqual([], data['playable_cards'])

    def test_get_current_player_name(self):
        player = Player('player')
        self.assertEqual('player', player.getCurrentPlayerName())

    def test_get_current_player_type(self):
        player = Player('player', 'b')
        self.assertEqual('b', player.getCurrentPlayerType())

    def test_draw_card(self):
        player = Player()
        hand = player.hand
        hand.append('card')
        player.draw_card('card')
        self.assertEqual(hand, player.hand)

    def test_get_playable_card_count(self):
        player = Player()
        self.assertEqual(0, player.get_playable_card_count())

    def test_get_playable_cards(self):
        player = Player()
        self.assertEqual([], player.get_playable_cards())

    def test_init_playable_cards_jack(self):
        player = Player()
        player.hand = ['card', 'jack_of_spades']
        player.init_playable_cards('jack_of_diamonds')
        self.assertEqual([0, 1], player.playable_cards)

    def test_init_playable_cards(self):
        player = Player()
        player.hand = ['card', 'three_of_spades']
        player.init_playable_cards('three_of_diamonds')
        self.assertEqual([1], player.playable_cards)

    def test_get_card_to_play(self):
        player = Player()
        player.hand = ['card', 'three_of_spades']
        self.assertEqual('card', player.get_card_to_play(0))

    def test_choose_card_human(self):
        input_device = Mock()
        player = Player('player', 'h', input_device=input_device)
        player.hand = ['card', 'three_of_spades']
        input_device.return_value = 0
        self.assertEqual('card', player.choose_card())

    @patch('player.time')
    def test_choose_card_bot(self, time):
        input_device = Mock()
        player = Player('player', 'b', input_device=input_device)
        player.hand = ['card', 'three_of_spades']
        input_device.return_value = 0
        self.assertEqual('card', player.choose_card())
        self.assertTrue(time.sleep.called)

    def test_check_mau_mau(self):
        player = Player()
        player.hand = ['card']
        self.assertEqual(1, player.check_mau())

    def test_check_mau_mau_mau(self):
        player = Player()
        player.hand = []
        self.assertEqual(0, player.check_mau())

    def test_get_card_count(self):
        player = Player()
        player.hand = ['card']
        self.assertEqual(1, player.get_card_count())

    def test_send(self):
        output_device = Mock()
        player = Player('player', 'h', output_device=output_device)
        player.send('message')
        self.assertTrue(output_device.called)

if __name__ == '__main__':
    unittest.main()

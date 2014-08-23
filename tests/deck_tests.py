from deck import Deck
import unittest


class DeckTestCase(unittest.TestCase):

    def test_get_current_middle(self):
        deck = Deck()
        self.assertEqual(deck.middle_card, deck.get_current_middle())

    def test_middle_to_stack(self):
        deck = Deck()
        current_deck = deck.deck
        current_middle = deck.get_current_middle()
        current_deck.append(current_middle)
        deck.middle_to_stack()
        self.assertEqual(current_deck, deck.deck)

    def test_new_middle(self):
        deck = Deck()
        deck.set_new_middle('card')
        self.assertEqual('card', deck.get_current_middle())

    def test_deal_card(self):
        deck = Deck()
        deck.deck[-1] = 'card'
        self.assertEqual('card', deck.deal_card())

    def test_get_random_card(self):
        Deck.get_random_card()

if __name__ == '__main__':
    unittest.main()

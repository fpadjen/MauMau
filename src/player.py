import time


class Player(object):
    def __init__(self,
                 name=None,
                 playerType=None,
                 output_device=None,
                 input_device=None):
        self.name = name
        self.hand = []
        self.playerType = playerType
        self.playable_cards = []
        self.output_device = output_device
        self.input_device = input_device

    def to_dict(self):
        return {
            'name': self.name,
            'hand': self.hand,
            'playable_cards': self.playable_cards
        }

    def getCurrentPlayerName(self):
        return self.name

    def getCurrentPlayerType(self):
        return self.playerType

    def draw_card(self, card):
        self.hand.append(card)

    def get_playable_card_count(self):
        return len(self.playable_cards)

    def get_playable_cards(self):
        return self.playable_cards

    def init_playable_cards(self, middle):
        self.playable_cards = []
        if "jack" in middle:
            self.playable_cards = [i for i, _ in enumerate(self.hand)]
            return
        middle_value, middle_color = middle.split('_of_')
        for card in range(0, len(self.hand)):
            if (middle_color in self.hand[card]
                    or middle_value in self.hand[card]):
                self.playable_cards.append(card)

    # FIXME: function name here should reflect human player
    def get_card_to_play(self, number):
        self.check_mau()
        return self.hand.pop(number)

    def choose_card(self):
        if self.getCurrentPlayerType() == 'h':
            return self.hand.pop(int(self.input_device()))
        time.sleep(1)
        return self.hand.pop(0)

    def check_mau(self):
        if len(self.hand) == 1:
            # mau
            return 1
        elif len(self.hand) == 0:
            # maumau
            return 0
        else:
            return 1

    def get_card_count(self):
        return len(self.hand)

    def send(self, message):
        if self.playerType == 'h':
            self.output_device(message)

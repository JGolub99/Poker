import random


class Card:
    def __init__(self, value, suit):
        self.suit = suit
        self.value = value
        self.face()

# Method to show card

    def show(self):
        print("{} of {}".format(self.value, self.suit))

# Method to convert numbers to letters

    def face(self):
        if self.value == 11:
            self.value = "J"
        if self.value == 12:
            self.value = "Q"
        if self.value == 13:
            self.value = "K"
        if self.value == 1:
            self.value = "A"


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

# Method to build a full deck

    def build(self):
        for s in ["Spades", "Clubs", "Hearts", "Diamonds"]:
            for v in range(1, 14):
                self.cards.append(Card(v, s))

# Method to show all cards in deck

    def show(self):
        for c in self.cards:
            c.show()

# Method to shuffle cards in deck

    def shuffle(self):
        for i in range(len(self.cards)-1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

# Method to draw 1 card from top of deck

    def draw(self):
        return self.cards.pop()


class Player:

    num_players = 0
    call_value = 0

    def __init__(self, name, stack):
        self.hand = []
        self.player_pot = 0
        self.name = name
        self.stack = stack
        Player.num_players += 1

# Method to draw card from a given deck, chainable

    def draw_card(self, d):
        self.hand.append(d.draw())
        return self

# Method to show full hand

    def show_hand(self):
        for c in self.hand:
            c.show()

# Action methods

    def fold(self):
        self.hand.clear()

    def bet(self, amount):
        self.player_pot = self.player_pot + amount
        self.stack = self.stack - amount
        Player.call_value = amount

    def call(self):
        self.call_value = Player.call_value - self.player_pot
        self.player_pot = self.player_pot + self.call_value
        self.stack = self.stack - self.call_value


class Board:

    def __init__(self, d):
        self.board = []
        self.draw_flop(d)

    def draw_card(self, d):
        self.board.append(d.draw())

# Methods for adding to the board:

    def draw_flop(self, d):
        self.draw_card(d)
        self.draw_card(d)
        self.draw_card(d)

    def draw_turn(self, d):
        self.draw_card(d)

    def draw_river(self, d):
        self.draw_card(d)

    def show_board(self):
        for c in self.board:
            c.show()


class Pot:

    def __init__(self, players):
        self.value = 0
        self.players = players

    def show_value(self):
        print(self.value)

    def collect_bets(self):
        for i in self.players:
            self.value = self.value + i.player_pot

    def empty_pot(self):
        self.value = 0


def main():
    deck = Deck()
    deck.shuffle()

    jacob = Player("Jacob", 2000)
    lia = Player("Lia", 1000)
    jacob.draw_card(deck).draw_card(deck)
    print(jacob.name, jacob.stack, ":")
    jacob.show_hand()
    print("")
    lia.draw_card(deck).draw_card(deck)
    print(lia.name, lia.stack, ":")
    lia.show_hand()
    print("")

    input("Draw flop: \n")
    board = Board(deck)
    board.show_board()
    print("")
    input("Draw turn: \n")
    board.draw_turn(deck)
    board.show_board()
    print("")
    input("Draw river: \n")
    board.draw_river(deck)
    board.show_board()


if __name__ == '__main__':
    main()

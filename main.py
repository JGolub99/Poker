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
    players = []

    fold_list = ["fold", "Fold", "FOLD"]
    call_list = ["call", "Call", "CALL"]
    bet_list = ["bet", "Bet", "BET"]
    raise_list = ["raise", "Raise", "RAISE"]
    check_list = ["check", "Check", "CHECK"]
    action_list = fold_list+call_list+bet_list+raise_list+check_list 

    def __init__(self, name, stack):
        self.hand = []
        self.player_pot = 0
        self.name = name
        self.stack = stack
        Player.num_players += 1
        Player.players.append(self)

# Method to draw card from a given deck, chainable

    def draw_card(self, d):
        self.hand.append(d.draw())
        return self

# Method to show full hand

    def show_hand(self):
        for c in self.hand:
            c.show()

# Method to reset call value between bets:
    @classmethod
    def reset_call(cls):
       cls.call_value=0


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

# Method to request action from player

    def action(self):
        x = input("{} action: ".format(self.name))
        x_list = x.split()
        if x_list[0] in Player.fold_list:
            self.fold()
        if x_list[0] in Player.bet_list:
            self.bet(int(x_list[1]))
        if x_list[0] in Player.call_list:
            self.call()
        if x_list[0] in Player.raise_list:
            if int(x_list[1])>Player.call_value:
               self.bet(int(x_list[1]))
            else:
                print("Illegal play ")
                self.action()
        if x_list[0] in Player.check_list:
            if Player.call_value>0:
                print("Illegal play ")
                self.action()
            else:
                self.bet(0)
        if x_list[0] not in Player.action_list:
            print("Illegal play ")
            self.action()
        
# Method to call upon all players for an action and reset call value:
    @classmethod
    def player_action(cls):
        for i in cls.players:
            i.action()
        cls.reset_call()


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

    jacob = Player("Jacob", 2000)
    lia = Player("Lia", 1000)
    i=0

    while i < 1:
        deck = Deck()
        deck.shuffle()
        jacob.draw_card(deck).draw_card(deck)
        print(jacob.name, jacob.stack, ":")
        jacob.show_hand()
        print("")
        lia.draw_card(deck).draw_card(deck)
        print(lia.name, lia.stack, ":")
        lia.show_hand()
        print("")
        Player.player_action()
        input("Draw flop: \n")
        board = Board(deck)
        board.show_board()
        print("")
        Player.player_action()
        input("Draw turn: \n")
        board.draw_turn(deck)
        board.show_board()
        print("")
        Player.player_action()
        input("Draw river: \n")
        board.draw_river(deck)
        board.show_board()
        Player.player_action()
        i+=1



if __name__ == '__main__':
    main()
import random
import itertools
import numpy as np

hands_dict = {
  0: "High Card",
  1: "One Pair",
  2: "Two Pair",
  3: "Three of a Kind",
  4: "Straight",
  5: "Flush",
  6: "Full House",
  7: "Four of a Kind",
  8: "Straight Flush"}


face_dict = {2: "Two", 3: 'Three', 4: 'Four', 5: 'Five',
    6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: 'Ten',
    11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}


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
    players_in_hand = []
    blinds_dict = {}
    dealer_position = 1

    fold_list = ["fold", "Fold", "FOLD"]
    call_list = ["call", "Call", "CALL"]
    bet_list = ["bet", "Bet", "BET"]
    raise_list = ["raise", "Raise", "RAISE"]
    check_list = ["check", "Check", "CHECK"]
    allin_list = ["all", "All", "ALL"]
    action_list = fold_list+call_list+bet_list+raise_list+check_list+allin_list 

    value_dict = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    value_dict.update((x, x) for x in range(2,11))

    def __init__(self, name, stack):
        self.hand = []
        self.temp_hand = [] # For comparing with board cards
        self.foldi = False
        self.player_pot = 0
        self.name = name
        self.stack = stack
        Player.num_players += 1
        Player.players.append(self)
        #Player.update_dict()   This was from an older blinds method

# Method to draw card from a given deck, chainable

    def draw_card(self, d):
        self.hand.append(d.draw())
        return self

# Method to show full hand

    def show_hand(self):
        for c in self.hand:
            c.show()

# Method to add winnings to stack

    def add_to_stack(self, amount):
        self.stack += amount

#Method to reset players_in_hand between folds and games:
    @classmethod
    def reset_players(cls):
        cls.players_in_hand.clear()
        for i in cls.players:
            if i.foldi == False:
               cls.players_in_hand.append(i)

# Method to reset call value between bets:
    @classmethod
    def reset_call(cls):
       cls.call_value=0

# Method to reset fold values to False for all players at table
    @classmethod
    def reset_folders(cls):
        for i in cls.players:
            i.foldi = False

# Method to discard all current hands
    @classmethod
    def discard_hands(cls):
        for i in cls.players:
            i.hand.clear()

# Method to collect blinds and move dealer button
# NOT REQUIRED ANYMORE!
    @classmethod
    def collect_blinds(cls, pot, big_blind):
        small_blind_position = cls.dealer_position+1
        small_blind_key = round((small_blind_position/cls.num_players)%1,2)
        big_blind_position = cls.dealer_position+2
        big_blind_key = round((big_blind_position/cls.num_players)%1,2)
        cls.players[cls.blinds_dict[small_blind_key]].stack-=0.5*big_blind
        cls.players[cls.blinds_dict[big_blind_key]].stack-=big_blind
        pot.increase_pot(1.5*big_blind)
        cls.dealer_position+=1

# Alternative method to collecting blinds
    @classmethod
    def collect_blinds_two(cls, big_blind):
        cls.players[1].bet(0.5*big_blind)
        cls.players[2].bet(big_blind) 

# Method to change order of play
    @classmethod
    def change_order(cls):
        cls.players = rotate(cls.players,1)

# Method to update the blinds dictionary
# NOT REQUIRED ANYMORE!
    @classmethod
    def update_dict(cls):
        cls.blinds_dict = {}
        keys = np.linspace(0,1,cls.num_players+1)[1:]
        outputs = range(0,cls.num_players)
        for i in outputs:
            cls.blinds_dict.update([(round(keys[i]%1,2),i)])

        

# Action methods

    def fold(self):
        self.hand.clear()
        self.foldi = True

    def bet(self, amount):
        self.player_pot = self.player_pot + amount
        self.stack = self.stack - amount
        Player.call_value = amount

    def call(self):
        self.call_value = Player.call_value - self.player_pot
        if self.call_value <= self.stack:
            self.player_pot = self.player_pot + self.call_value
            self.stack = self.stack - self.call_value
        else:
            self.player_pot = self.player_pot + self.stack
            self.stack = 0

# Method to request action from player

    def action(self):
        if self.stack!=0:
            x = input("{} action: ".format(self.name))
            x_list = x.split()
            if x_list[0] in Player.fold_list:
                self.fold()
            if x_list[0] in Player.bet_list:
                if int(x_list[1])>self.stack or Player.call_value>0:
                    print("Illegal play ")
                    self.action()
                else:
                    self.bet(int(x_list[1]))
            if x_list[0] in Player.allin_list:
                self.bet(self.stack)
            if x_list[0] in Player.call_list:
                if Player.call_value == 0:
                    print("Illegal play ")
                    self.action()
                else:
                    self.call()
            if x_list[0] in Player.raise_list:
                if int(x_list[1])>Player.call_value and int(x_list[1])<=(self.stack+self.player_pot):
                   self.bet(int(x_list[1]))
                else:
                    print("Illegal play ")
                    self.action()
            if x_list[0] in Player.check_list:
                if Player.call_value>0 and Player.call_value!=self.player_pot:
                    print("Illegal play ")
                    self.action()
                else:
                    self.bet(0)
            if x_list[0] not in Player.action_list:
                print("Illegal play ")
                self.action()
        
# Method to call upon all players for an action and reset call value:
    @classmethod
    def player_action(cls, round1=True):
        if len(cls.players_in_hand)>1:
            if round1==True:
                for i in cls.players_in_hand:
                    i.action()
                    print(i.player_pot, i.stack)
                cls.reset_players()
                for i in cls.players_in_hand:
                    if i.player_pot < cls.call_value and i.stack !=0:
                        cls.player_action(False)
            elif round1==False:
                for i in cls.players_in_hand:
                    if i.player_pot < cls.call_value:
                        i.action()
                        print(i.player_pot, i.stack)
                cls.reset_players()
                for i in cls.players_in_hand:
                    if i.player_pot < cls.call_value and i.stack !=0:
                        cls.player_action(False)
            cls.reset_call()

# Method to provide all necessary information to determine hand and 
# tie breaker. REQUIRE FIVE CARDS.

    def eval_hand(self, setting=1):
        if setting == 1:
            hand = self.hand
        elif setting == 2:
            hand = self.temp_hand
        values = sorted([Player.value_dict[c.value] for c in hand], reverse=True)
        suits = [c.suit for c in hand]
        straight = (values == list(range(values[0], values[0]-5, -1))
                    or values == [14, 5, 4, 3, 2])
        flush = all(s == suits[0] for s in suits)

        if straight and flush: return 8, "palceholder", values
        if flush: return 5, "placeholder", values
        if straight: return 4, "placeholder", values

        trips = []
        pairs = []
        for v, group in itertools.groupby(values):
            count = sum(1 for _ in group)
            if count == 4: return 7, v, values
            elif count == 3: trips.append(v)
            elif count == 2: pairs.append(v)

        if trips: return (6 if pairs else 3), trips, values, pairs
        return len(pairs), pairs, values
    
    @classmethod
    def find_winner(cls):
        winner = [cls.players_in_hand[0]]
        for i in range(1, len(cls.players_in_hand)):
            temp = compare_hands(winner[0], cls.players_in_hand[i])[1]
            if temp=="Split pot":
                winner.append(cls.players_in_hand[i])
            else:
                winner = [temp]
        return winner


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
    
    def clear_board(self):
        self.board = []


class Pot:

    def __init__(self, players):
        self.value = 0
        self.players = players

    def show_value(self):
        print(self.value)

    def collect_bets(self):
        for i in self.players:
            self.value = self.value + i.player_pot
            i.player_pot = 0

    def empty_pot(self):
        self.value = 0
    
    def increase_pot(self, amount):
        self.value = self.value+amount
    
    def decrease_pot(self, amount):
        self.value = self.value-amount

# This function translates the output of the hand evaluator to a statement
# in English for the player.

def hand_interpreter(my_tuple):
    hand = hands_dict[my_tuple[0]]
    my_card = " "
    if hand == "High Card":
        my_card = my_tuple[2][0]
        my_card = face_dict[my_card]
        return hand + ": " + my_card
    if hand == "One Pair":
        my_card = my_tuple[1][0]
        my_card = face_dict[my_card]
        return hand + ": " + my_card + "s"
    if hand == "Two Pair":
        my_card1 = face_dict[my_tuple[1][0]]
        my_card2 = face_dict[my_tuple[1][1]]
        return hand + ": " + my_card1 + "s and " + my_card2 + "s" 
    if hand == "Three of a Kind":
        my_card = my_tuple[1][0]
        my_card = face_dict[my_card]
        return hand + ": " + my_card + "s"
    if hand == "Straight":
        if all(x in my_tuple[2] for x in [14, 5]):
            my_card = "Five"
        else:
            my_card = my_tuple[2][0]
            my_card = face_dict[my_card]
        return my_card + " high " + hand
    if hand == "Flush":
        my_card = my_tuple[2][0]
        my_card = face_dict[my_card]
        return my_card + " high " + hand
    if hand == "Full House":
        my_card1 = face_dict[my_tuple[1][0]]
        my_card2 = face_dict[my_tuple[3][0]]
        return my_card1 + "s full of " + my_card2 + "s"
    if hand == "Four of a Kind":
        my_card = face_dict[my_tuple[1]]
        return hand + ": " + my_card + "s"
    if hand == "Straight Flush":
        if all(x in my_tuple[2] for x in [14, 13]):
            return "Royal Flush"
        if all(x in my_tuple[2] for x in [14, 5]):
            my_card = "Five"
            return my_card + " high " + hand
        else:
            my_card = face_dict[my_tuple[2][0]]
            return my_card + " high " + hand

# This function compares two hands, either for 1 or 2 players.

def compare_hands(player1, player2=None):
    score1 = player1.eval_hand(1)
    if player2==None:
        score2 = player1.eval_hand(2)
        if score1[0]<score2[0]:
            #print("Score 2 wins")
            return player1.temp_hand, player1
    else:
        score2 = player2.eval_hand(1)
        if score1[0]<score2[0]:
            #print("Score 2 wins")
            return player2.hand, player2
    
    if score1[0]>score2[0]:
        #print("Score 1 wins")
        return player1.hand, player1
    
    if score1[0]==score2[0]:
        #print("Tie")
        if score1[0]==0 or score1[0]==4 or score1[0]==5 or score1[0]==8:
            i = 0
            ans = "Tie"
            while i <= 4 and ans == "Tie":
                ans = highcard_tiebreak(score1[2], score2[2], i)
                if ans == "One":
                    return player1.hand, player1
                elif ans == "Two" and player2 == None:
                    return player1.temp_hand, player1
                elif ans == "Two" and player2 != None:
                    return player2.hand, player2
                i+=1
            if i==5 and player2 == None:
                return player1.hand, player1
            elif i==5 and player2!=None:
                return "placeholder", "Split pot"
        elif score1[0]==1 or score1[0]==3 or score1[0]==7:
            if score1[1]>score2[1]:
                return player1.hand, player1
            elif score1[1]<score2[1] and player2==None:
                return player1.temp_hand, player1
            elif score1[1]<score2[1] and player2!=None:
                return player2.hand, player2
            elif score1[1]==score2[1]:
                i = 0
                ans = "Tie"
                while i <= 4 and ans == "Tie":
                    ans = highcard_tiebreak(score1[2], score2[2], i)
                    if ans == "One":
                        return player1.hand, player1
                    elif ans == "Two" and player2 == None:
                        return player1.temp_hand, player1
                    elif ans == "Two" and player2 != None:
                        return player2.hand, player2
                    i+=1
                if i==5 and player2==None:
                    return player1.hand, player2
                elif i==5 and player2!=None:
                    return "placeholder", "Split pot"
        elif score1[0]==2:
            if score1[1][0]>score2[1][0]:
                return player1.hand, player1
            elif score1[1][0]<score2[1][0] and player2==None:
                return player1.temp_hand, player1
            elif score1[1][0]<score2[1][0] and player2!=None:
                return player2.hand, player2
            elif score1[1][0]==score2[1][0]:
                if score1[1][1]>score2[1][1]:
                    return player1.hand, player1
                elif score1[1][1]<score2[1][1] and player2==None:
                    return player1.temp_hand, player1
                elif score1[1][1]<score2[1][1] and player2!=None:
                    return player2.hand, player2
                elif score1[1][1]==score2[1][1]:
                    i = 0
                    ans = "Tie"
                    while i <= 4 and ans == "Tie":
                        ans = highcard_tiebreak(score1[2], score2[2], i)
                        if ans == "One":
                            return player1.hand, player1
                        elif ans == "Two" and player2 == None:
                            return player1.temp_hand, player1
                        elif ans == "Two" and player2 != None:
                            return player2.hand, player2
                        i+=1
                    if i==5 and player2==None:
                        return player1.hand, player1
                    elif i==5 and player2!=None:
                        return "placeholder", "Split pot"
        elif score1[0]==6:
            if score1[1][0]>score2[1][0]:
                return player1.hand, player1
            elif score1[1][0]<score2[1][0] and player2==None:
                return player1.temp_hand, player1
            elif score1[1][0]<score2[1][0] and player2!=None:
                return player2.hand, player2
            elif score1[1][0]==score2[1][0]:
                if score1[3][0]>score2[3][0]:
                    return player1.hand, player1
                elif score1[3][0]<score2[3][0] and player2==None:
                    return player1.temp_hand, player1
                elif score1[3][0]<score2[3][0] and player2!=None:
                    return player2.hand, player2
                elif score1[3][0]==score2[3][0]:
                    i = 0
                    ans = "Tie"
                    while i <= 4 and ans == "Tie":
                        ans = highcard_tiebreak(score1[2], score2[2], i)
                        if ans == "One":
                            return player1.hand, player1
                        elif ans == "Two" and player2 == None:
                            return player1.temp_hand, player1
                        elif ans == "Two" and player2 != None:
                            return player2.hand, player2
                        i+=1
                    if i==5 and player2==None:
                        return player1.hand, player1
                    elif i==5 and player2!=None:
                        return "placeholder", "Split pot"

                
# This function breaks high card ties.

def highcard_tiebreak(vals1, vals2, iter):
    if vals1[iter]>vals2[iter]:
        return "One"
    elif vals1[iter]<vals2[iter]:
        return "Two"
    elif vals1[iter]==vals2[iter]:
        return "Tie"

# This function accepts a player and board to determine the player's
# best possible hand.

def find_best_hand(player, myboard):
    list_of_cards = player.hand + myboard.board
    combinations = list(itertools.combinations(list_of_cards,5))
    player.hand = list(combinations[0])
    for i in range(1,21):
        player.temp_hand = list(combinations[i])
        player.hand = compare_hands(player)[0]
    return hand_interpreter(player.eval_hand())    

# This function rotates a list

def rotate(l, n):
    return l[n:] + l[:n]


def main():

    jacob = Player("Jacob", 2000)
    lia = Player("Lia", 1000)
    sam = Player("Sam", 1000)
    i=0
    pot = Pot(Player.players)

    while i < 2:
        print("")
        deck = Deck()
        deck.shuffle()
        pot.empty_pot()
        Player.reset_players()
        Player.collect_blinds_two(100)
        jacob.draw_card(deck).draw_card(deck)
        print(jacob.name, jacob.stack, ":")
        jacob.show_hand()
        print("")
        lia.draw_card(deck).draw_card(deck)
        print(lia.name, lia.stack, ":")
        lia.show_hand()
        print("")
        sam.draw_card(deck).draw_card(deck)
        print(sam.name, sam.stack, ":")
        sam.show_hand()
        print("")
        Player.player_action()
        pot.collect_bets()
        input("Draw flop: \n")
        board = Board(deck)
        board.show_board()
        print("")
        Player.player_action()
        pot.collect_bets()
        input("Draw turn: \n")
        board.draw_turn(deck)
        board.show_board()
        print("")
        Player.player_action()
        pot.collect_bets()
        input("Draw river: \n")
        board.draw_river(deck)
        board.show_board()
        print("")
        Player.player_action()
        pot.collect_bets()
        print("")
        for j in Player.players_in_hand:
            print(j.name,", ", find_best_hand(j,board))
            j.show_hand()
            print("")
        winner = Player.find_winner()
        if len(winner)>1:
            print("Split pot!")
            winnings = pot.value/len(winner)
            for k in winner:
                k.add_to_stack(winnings)
        else:
            print(winner[0].name + " wins!")
            winner[0].add_to_stack(pot.value)
            print(winner[0].stack)
        pot.empty_pot()
        Player.reset_folders()
        Player.discard_hands()
        i+=1
        Player.change_order()
        input("\n Next game: ")



if __name__ == '__main__':
    main()


#jacob = Player("Jacob", 2000)
#deck = Deck()
#deck.shuffle()
#jacob.temp_hand.append(Card(10,"Hearts"))
#jacob.temp_hand.append(Card(1,"Hearts"))
#jacob.temp_hand.append(Card(13,"Hearts"))
#jacob.temp_hand.append(Card(12,"Hearts"))
#jacob.temp_hand.append(Card(11,"Hearts"))
#jacob.draw_card(deck).draw_card(deck).draw_card(deck).draw_card(deck).draw_card(deck)
#jacob.show_hand()
#print(jacob.eval_hand(2))
#print(hand_interpreter(jacob.eval_hand(2)))

#jacob = Player("Jacob", 2000)
#deck = Deck()
#deck.shuffle()
#jacob.hand.append(Card(11,"Spades"))
#jacob.hand.append(Card(9,"Spades"))
#my_board=Board(deck)
#my_board.clear_board()
#my_board.board.append(Card(7,"Hearts"))
#my_board.board.append(Card(11,"Hearts"))
#my_board.board.append(Card(9,"Diamonds"))
#my_board.board.append(Card(9,"Clubs"))
#my_board.board.append(Card(11,"Diamonds"))
#print(find_best_hand(jacob, my_board))


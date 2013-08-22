# Playing Cards 2.0
# Demonstrates inheritance - class extension

class Card(object):
    """ A playing card. """
    RANKS = ["A", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "J", "Q", "K"]
    SUITS = ["c", "d", "h", "s"]

    def __init__(self, rank, suit):
        self.rank = rank 
        self.suit = suit

    def __str__(self):
        rep = self.rank + self.suit
        return rep

class Hand(object):
    """ A hand of playing cards. """
    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
           rep = ""
           for card in self.cards:
               rep += str(card) + "\t"
        else:
            rep = "<empty>"
        return rep

    def clear(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)

class Deck(Hand):
    """ A deck of playing cards. """
    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS: 
                self.add(Card(rank, suit))

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self, hands, per_hand = 1):
        for rounds in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.give(top_card, hand)
                else:
                    print("Can't continue deal. Out of cards!")


# main
deck1 = Deck()
print("Created a new deck.")
print("Deck:")
print(deck1)

deck1.populate()
print("\nPopulated the deck.")
print("Deck:")
print(deck1)

deck1.shuffle()
print("\nShuffled the deck.")
print("Deck:")
print(deck1)

my_hand = Hand()
your_hand = Hand()
hands = [my_hand, your_hand]
deck1.deal(hands, per_hand = 5)
print("\nDealt 5 cards to my hand and your hand.")
print("My hand:")
print(my_hand)
print("Your hand:")
print(your_hand)
print("Deck:")
print(deck1)

deck1.clear()
print("\nCleared the deck.")
print("Deck:", deck1)

input("\n\nPress the enter key to exit.")

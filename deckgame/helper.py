"""
This module implements the required classes and methods of the game.
It comprises the Player, Card and CardsCollection classes.
"""
import random


class Player(object):
    """
    Simulates a player.
    """
    def __init__(self, name, health=30, handsize=5):
        """
        Initialises a Player instance.

        :param name: player's name
        :param health: player's starting health (default=30)
        :param handsize: player's hand size (default=5)
        """
        self._name = name
        self._health = health
        self._handsize = handsize
        self._strength = 0
        self._money = 0
        self._attack = 0
        self._deck = CardsCollection()
        self._hand = CardsCollection()
        self._active = CardsCollection()
        self._discard = CardsCollection()

    @property
    def name(self):
        """
        Player's name getter.

        :return self._name: player's name
        """
        return self._name

    @property
    def health(self):
        """
        Player's health getter.

        :return self._health: player's health value
        """
        return self._health

    @property
    def handsize(self):
        """
        Player's hand maximum size getter.

        :return self._handsize: player's hand maximum size
        """
        return self._handsize

    @property
    def strength(self):
        """
        Player's strength getter.

        :return self._strength: player's strength value
        """
        return self._strength

    @property
    def money(self):
        """
        Player's money getter.

        :return self._money: player's money value
        """
        return self._money

    @property
    def attack(self):
        """
        Player's attack getter.

        :return self._attack: player's attack value
        """
        return self._attack

    @property
    def deck(self):
        """
        Player's deck getter.

        :return self._deck: player's deck (a CardsCollection() object)
        """
        return self._deck

    @property
    def hand(self):
        """
        Player's hand getter.

        :return self._hand: player's hand (a CardsCollection() object)
        """
        return self._hand

    @property
    def active(self):
        """
        Player's active area getter.

        :return self._active: player's active area (a CardsCollection()
        object)
        """
        return self._active

    @property
    def discard(self):
        """
        Player's discard pile getter.

        :return self._discard: player's discard pile (a CardsCollection()
        object)
        """
        return self._discard

    def init_hand(self):
        """
        Initialises player's hand using his deck (or his discard pile
        if deck is empty).
        """
        for _ in range(self._handsize):
            if self._deck.size() == 0:
                self._discard.shuffle_collection()
                self._deck.replace(self._discard)
                self._discard.clear_collection()
            card = self._deck.pop()
            self._hand.push(card)

    def init_deck(self):
        """
        Initialises player's deck.
        """
        self._deck.push(Card('Serf', 0, 1, 0), 8)
        self._deck.push(Card('Squire', 1, 0, 0), 2)

    def play_all(self):
        """
        Drops all the cards from player's hand (if any) to his active area.
        """
        for _ in range(self._hand.size()):
            card = self._hand.pop()
            self._active.push(card)
            self._money = self._money + card.money
            self._attack = self._attack + card.attack
        print '\nPlayed all cards!'

    def play_card(self, index):
        """
        Drops the cards with the given index from player's hand to his active area.

        :param index: card's index on player's hand
        """
        if index < self._hand.size():
            card = self._hand.pop(index)
            self._active.push(card)
            self._money = self._money + card.money
            self._attack = self._attack + card.attack
            print '\nCard played:\n%s' % card
        else:
            print "\nInvalid index number! Please type a valid number!"

    def attack_opponent(self, opponent):
        """
        Attacks an opponent.

        :param opponent: the opponent to attack (a Player() instance)
        """
        opponent._health = opponent._health - self._attack
        self._attack = 0

    def buy_supplement(self, supplement):
        """
        Buys the top supplement.

        :param supplement: a list of available supplements
        """
        self._money = self._money - supplement.cards[supplement.size() - 1].cost
        card = supplement.pop()
        self._discard.push(card)
        self._strength = self._strength + card.attack
        print "\nSupplement bought:\n%s" % card

    def buy_card(self, central_active, central_deck, index):
        """
        Buys the card with the given from central active area.

        :param central_active: a CardsCollection() object that contains the
        cards of the central active area
        :param central_active: a CardsCollection() object that contains the
        cards of the central deck area
        :param index: the index of the card to be bought on central active area
        """
        self._money = self._money - central_active.cards[index].cost
        card = central_active.pop(index)
        self._discard.push(card)
        self._strength = self._strength + card.attack
        print "\nCard bought:\n%s" % card

        if central_deck.size() > 0:
            card = central_deck.pop()
            central_active.push(card)

    def end_turn(self):
        """
        Ends player's turn. It moves any cards from player's hand and active
        area on his discard pile and generates a new hand from his deck.
        """
        for _ in range(self._hand.size()):
            card = self._hand.pop()
            self._discard.push(card)

        for _ in range(self._active.size()):
            card = self._active.pop()
            self._discard.push(card)

        for _ in range(self._handsize):
            if self._deck.size() == 0:
                self._discard.shuffle_collection()
                self._deck.replace(self._discard)
                self._discard.clear_collection()
            card = self._deck.pop()
            self._hand.push(card)
        self._money = 0
        self._attack = 0

    def print_values(self):
        """
        Prints player's money and attack values.
        """
        print "Money %s, Attack %s" % (self._money, self._attack)

    def compute_strength(self):
        """
        Computes player's strength and stores it in a variable. This method
        actually computes player's strength on game's start. Any additional cards
        that are bought by the player are considered on-the-fly, contributing
        their strength in the buy_card and buy_supplement methods.
        """
        for card in self._deck.cards:
            self._strength = self._strength + card.attack

class Card(object):
    """
    Simulates a card.
    """
    def __init__(self, name, attack=0, money=0, cost=0):
        """
        Initialises a Card instance.

        :param name: card's name
        :param attack: card's attack strength (default=0)
        :param money: card's money strength (default=0)
        :param cost: card's cost (default=0)
        """
        self._name = name
        self._money = money
        self._attack = attack
        self._cost = cost

    @property
    def name(self):
        """
        Card's name getter.

        :return self._name: card's name
        """
        return self._name

    @property
    def money(self):
        """
        Card's money strength getter.

        :return self._money: card's money strength
        """
        return self._money

    @property
    def attack(self):
        """
        Card's attack strength getter.

        :return self._attack: card's attack strength
        """
        return self._attack

    @property
    def cost(self):
        """
        Card's attack strength getter.

        :return self._attack: card's attack strength
        """
        return self._cost

    def __str__(self):
        """
        Called when str method is invoked for a card instance.

        :return: a string that represents card's content
        """
        return 'Name: %s, costing %s with attack %s and money %s' % \
            (self._name, self._cost, self._attack, self._money)

class CardsCollection(object):
    """
    Simulates a collection of cards.
    """
    def __init__(self):
        """
        Initialises a CardCollection instance.
        """
        self._cards = []

    @property
    def cards(self):
        """
        Cards' list getter.

        :return self._cards: a list of cards
        """
        return self._cards

    def shuffle_collection(self):
        """
        Shuffles collection's cards
        """
        random.shuffle(self._cards)

    def clear_collection(self):
        """
        Clears collection's list of cards
        """
        self._cards = []

    def replace(self, collection):
        """
        Replaces collection's cards with the cards of the given collection.

        :param collection: a CardsCollection() instance
        """
        self._cards = collection.cards

    def push(self, card, times=1):
        """
        Appends a card to the cards' list (multiple times, i case the
        corresponding parameter is given).

        :param card: the card to be added to the collection (a Card instance)
        :param times, number of identical cards to be added
        """
        self._cards.extend(times * [card])

    def pop(self, index=-1):
        """
        Removes a card from cards' list based on the given index (top card by default).

        :param index: the index of the card to be removed
        """
        return self._cards.pop(index)

    def size(self):
        """
        Returns the size of the cards list

        :return the size of the cards list
        """
        return len(self._cards)

    def print_collection(self, indexes=False):
        """
        Prints the collection's cards (and their indexes, in case the appropriate parameter is set).

        :param indexes: if True the method prints the indexes of the cards as well
        """
        if indexes:
            for i in range(self.size()):
                print "[%s] %s" % (i, self._cards[i])
        else:
            for i in range(self.size()):
                print self._cards[i]

    def print_card(self, index=0):
        """
        Prints the card with the given index.

        :param index: the index of the card in the collection
        """
        print self._cards[index]

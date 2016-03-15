"""
Testing the Player class.
"""

import sys
import StringIO
import unittest

from deckgame.helper import Player, Card, CardsCollection

class MyTest(unittest.TestCase):
    """
    Tests for the Player class.
    """
    def setUp(self):
        """
        Suppresses print statements from original code.
        """
        self.actualstdout = sys.stdout
        sys.stdout = StringIO.StringIO()

    def test_player_init_(self):
        """
        Tests the initialiser of the class.
        """
        player = Player('Nikos', health=20, handsize=3)
        self.assertEqual(player.name, 'Nikos')
        self.assertEqual(player.health, 20)
        self.assertEqual(player.handsize, 3)

    def test_player_init_deck(self):
        """
        Tests the deck initialiser.
        """
        player = Player('Nikos')
        player.init_deck()
        self.assertEqual(player.deck.cards[0].name, 'Serf')

    def test_player_init_hand(self):
        """
        Tests the hand initialiser.
        """
        player = Player('Nikos')
        player.init_deck()
        player.init_hand()
        self.assertEqual(player.hand.size(), 5)

    def test_player_init_hand_empty_deck(self):
        """
        Tests the hand initialiser in case of empty deck. The expected
        behaviour of the system is to shuffle the discard pile's cards and
        generate a new deck from them. 
        """
        player = Player('Nikos')
        player.init_deck()
        player.discard.replace(player.deck)
        player.deck.clear_collection()
        player.init_hand()
        self.assertEqual(player.hand.size(), 5)
        self.assertEqual(player.discard.size(), 0)
        self.assertNotEqual(player.deck.size(), 0)

    def test_player_play_all(self):
        """
        Tests the play_all method.
        """
        player = Player('Nikos', health=20, handsize=5)
        player.init_deck()
        player.init_hand()
        player.play_all()
        self.assertEqual(player.hand.size(), 0)
        self.assertEqual(player.active.size(), 5)

    def test_player_play_card(self):
        """
        Tests the play_card method.
        """
        player = Player('Nikos')
        player.init_deck()
        player.init_hand()
        player.play_card(0)
        self.assertEqual(player.hand.size(), 4)
        self.assertEqual(player.active.size(), 1)
        player.play_card(6)
        self.assertEqual(player.hand.size(), 4)
        self.assertEqual(player.active.size(), 1)

    def test_player_attack_opponent(self):
        """
        Tests the attack method. This method only checks whether the attack
        action works properly.Any validation checks are conducted in parent
        methods and are thus checked using alternative test cases.
        """
        player_1 = Player('Nikos', health=30)
        player_pc = Player('Computer', health=30)
        player_1._attack = 5
        player_1.attack_opponent(player_pc)
        self.assertEqual(player_pc.health, 25)
        self.assertEqual(player_1.attack, 0)

    def test_player_buy_supplement(self):
        """
        Tests the buy_supplement method. This method only checks whether the attack
        action works properly.Any validation checks are conducted in parent
        methods and are thus checked using alternative test cases.
        """
        player = Player('Nikos')
        player._money = 2
        central = {'deck': CardsCollection(),
                   'active': CardsCollection(),
                   'supplement': CardsCollection(),
                   'active_size': 5}
        central['supplement'].push(Card('Levy', 1, 2, 2), 10)
        player.buy_supplement(central['supplement'])
        self.assertEqual(central['supplement'].size(), 9)
        self.assertEqual(player.discard.size(), 1)
        self.assertEqual(player.money, 0)

    def test_player_buy_card(self):
        """
        Tests the buy_card method. This method only checks whether the attack
        action works properly.Any validation checks are conducted in parent
        methods and are thus checked using alternative test cases.
        """
        player = Player('Nikos')
        player._money = 10
        central = {'deck': CardsCollection(),
                   'active': CardsCollection(),
                   'supplement': CardsCollection(),
                   'active_size': 5}
        central['deck'].push(Card('Deck card', 3, 0, 2), 1)
        central['active'].push(Card('Archer', 3, 0, 2), 5)
        player.buy_card(central['active'], central['deck'], 0)
        self.assertEqual(central['active'].size(), 5)
        self.assertEqual(player.discard.size(), 1)
        self.assertEqual(player.discard.cards[0].name, 'Archer')
        self.assertEqual(central['active'].cards[4].name, 'Deck card')
        player.buy_card(central['active'], central['deck'], 0)
        # deck size = 0 now -> no more cards from deck to active area
        self.assertEqual(central['active'].size(), 4)
        self.assertEqual(player.discard.size(), 2)

    def test_player_end_turn(self):
        """
        Tests the end_turn method with 0 cards in player's deck.
        Player's discard pile is shuffled and its cards go to player's deck.
        A new hand with handsize cards is generated from player's deck.
        """
        player = Player('Nikos', handsize=5)
        player.hand.push(Card('Archer', 3, 0, 2), 1)
        player.discard.push(Card('Archer', 3, 0, 2), 10)
        player.active.push(Card('Archer', 3, 0, 2), 4)
        player.end_turn()
        self.assertEqual(player.active.size(), 0)
        self.assertEqual(player.discard.size(), 0)
        self.assertEqual(player.deck.size(), 10)
        self.assertEqual(player.hand.size(), 5)

    def tearDown(self):
        """
        Resets stdout
        """
        sys.stdout = self.actualstdout

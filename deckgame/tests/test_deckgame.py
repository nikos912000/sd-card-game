"""
Testing the DeckGame class.
"""

import sys
import StringIO
import unittest
from mock import patch

from deckgame.helper import Player, Card
from deckgame.game import Game

class MyTest(unittest.TestCase):
    """
    Tests for the DeckGame class.
    """
    def setUp(self):
        """
        Suppresses print statements from original code.
        """
        self.actualstdout = sys.stdout
        sys.stdout = StringIO.StringIO()

    def test_player_turn(self):
        """
        Tests the player_turn method mocking user's input.
        It gives valid as well as invalid input, covering all possible
        branches.
        """
        deck_game = Game()
        deck_game.init_central_deck()
        deck_game.player_1.init_deck()
        deck_game.central['active'].push(Card('Archer', 1, 3, 3), 5)
        deck_game.player_1.hand.push(Card('Archer', 1, 0, 0))
        deck_game.player_1.hand.push(Card('Archer', 0, 1, 0))
        deck_game.player_1.hand.push(Card('Archer', 1, 1, 1))
        deck_game.player_1.hand.push(Card('Archer', 2, 2, 3), 2)
        deck_size = deck_game.player_1.deck.size()
        with patch('__builtin__.raw_input', side_effect=
                   ['0', '0', 'A', 'P', 'B', '0', 'B', '0', 'A']):
            deck_game.player_1_turn()
            self.assertEquals(deck_game.player_1.hand.size(), 5)
            self.assertEquals(deck_game.player_1.deck.size(), deck_size - 5)

    def test_aggressive_opponent(self):
        """
        Tests the get_opponent method mocking user's input.
        It gives an invalid input at first and a valid one for an aggressive
        opponent after that.
        """
        deck_game = Game()
        with patch('__builtin__.raw_input', side_effect=['b', 'a']):
            self.assertTrue(deck_game.get_opponent())

    def test_acquisative_opponent(self):
        """
        Tests the get_opponent method mocking user's input for an acquisative
        opponent.
        """
        deck_game = Game()
        with patch('__builtin__.raw_input', return_value='q'):
            self.assertFalse(deck_game.get_opponent())

    def test_set_up_game(self):
        """
        Tests the set_up method.
        """
        deck_game = Game()
        deck_game.set_up_game()
        self.assertEqual(deck_game.player_1.deck.size(), deck_game.player_pc.deck.size())
        self.assertEqual(deck_game.player_1.hand.size(), deck_game.player_1.handsize)
        self.assertEqual(deck_game.player_pc.hand.size(), deck_game.player_pc.handsize)
        self.assertGreater(deck_game.central['deck'].size(), 0)

    def test_init_central_deck(self):
        """
        Tests whether the central deck size is the expected one after
        initialising the deck.
        """
        deck_game = Game()
        deck_game.init_central_deck()
        self.assertEqual(deck_game.central['deck'].size(), 36)

    def test_buy_supplement(self):
        """
        Tests the buy_supplement method mocking user's input.
        """
        deck_game = Game()
        deck_game.player_1._money = 6
        deck_game.central['supplement'].push(Card('Archer', 3, 3, 6))
        with patch('__builtin__.raw_input', return_value='S'):
            deck_game.player_1_buy()
            self.assertEqual(deck_game.player_1.money, 0)
            self.assertEqual(deck_game.central['supplement'].size(), 0)

    def test_buy_card(self):
        """
        Tests the buy_card method mocking user's input.
        """
        deck_game = Game()
        deck_game.player_1._money = 3
        deck_game.central['active'].push(Card('Archer', 2, 2, 3))
        with patch('__builtin__.raw_input', return_value='0'):
            deck_game.player_1_buy()
            self.assertEqual(deck_game.player_1.money, 0)
            self.assertEqual(deck_game.central['active'].size(), 0)

    def test_buy_card_invalid_index(self):
        """
        Tests the card method mocking user's input and giving an invalid index
        for the card to buy.
        """
        deck_game = Game()
        deck_game.player_1._money = 3
        deck_game.central['active'].push(Card('Archer', 2, 2, 3))
        with patch('__builtin__.raw_input', side_effect=['1', 'E']):
            deck_game.player_1_buy()
            self.assertEqual(deck_game.player_1.money, 3)
            self.assertEqual(deck_game.central['active'].size(), 1)

    def test_player_pc_turn(self):
        """
        Tests the player_pc_turn method.
        """
        deck_game = Game()
        deck_game.aggressive = True
        deck_game.set_up_game()
        pc_ds = deck_game.player_pc.deck.size()
        deck_game.player_pc_turn()
        self.assertEqual(deck_game.player_pc.deck.size(), pc_ds - 5)

    def test_computer_buy(self):
        """
        Tests the computer_buy method.
        """
        deck_game = Game()
        deck_game.aggressive = True
        deck_game.player_pc._money = 3
        deck_game.central['active'].push(Card('Archer', 2, 2, 3))
        deck_game.central['active'].push(Card('Test1', 3, 1, 3))
        deck_game.central['active'].push(Card('Test2', 0, 4, 3))
        deck_game.central['supplement'].push(Card('Archer', 3, 3, 6))
        deck_game.computer_buy()
        self.assertEqual(deck_game.player_pc.discard.cards[0].name, 'Test1')

    def test_best_buy_aggressive(self):
        """
        Tests the computer_best_buy method for an aggressive opponent.
        The index returned should abide by the implemented logic.
        """
        deck_game = Game()
        deck_game.aggressive = True
        temp_list = [("S", Card('Archer', 2, 1, 2)),
                     (1, Card('Test1', 2, 2, 1)),
                     (3, Card('Test2', 1, 2, 1))]
        deck_game.computer_best_buy(temp_list)
        self.assertEqual(deck_game.computer_best_buy(temp_list), 1)

    def test_best_buy_acquisative(self):
        """
        Tests the computer_best_buy method for an acquisative opponent.
        The index returned should abide by the implemented logic.
        """
        deck_game = Game()
        deck_game.aggressive = False
        temp_list = [("S", Card('Archer', 3, 1, 5)),
                     (1, Card('Test1', 1, 3, 3)),
                     (3, Card('Test2', 0, 3, 2))]
        deck_game.computer_best_buy(temp_list)
        self.assertEqual(deck_game.computer_best_buy(temp_list), 2)

    def test_check_winner_player_1(self):
        """
        Tests the get_winner method where the winner is player_1.
        """
        deck_game = Game()
        deck_game.player_1 = Player('Nikos')
        deck_game.player_pc = Player('Computer')
        deck_game.player_1_health = 0
        self.assertTrue(deck_game.check_winner(), 'True expected. Player 1 wins.')

    def test_check_winner_player_pc(self):
        """
        Tests the get_winner method where the winner is player_pc.
        """
        deck_game = Game()
        deck_game.player_1 = Player('Nikos')
        deck_game.player_pc = Player('Computer')
        deck_game.player_pc._health = 0
        self.assertTrue(deck_game.check_winner(), 'True expected. Player PC wins.')

    def test_check_no_winner(self):
        """
        Tests the get_winner method where no winner found
        (and the game continues).
        """
        deck_game = Game()
        deck_game.player_1 = Player('Nikos')
        deck_game.player_pc = Player('Computer')
        deck_game.central['active'].push(Card('Archer', 3, 1, 5))
        deck_game.central['active'].push(Card('Test1', 1, 3, 3))
        deck_game.central['active'].push(Card('Test2', 0, 3, 2))
        self.assertFalse(deck_game.check_winner(),\
            'False expected. Players\' health > 0 and central.active.size() > 0')

    def test_check_winner_empty_active(self):
        """
        Tests the get_winner method for empty central deck.
        In this case the game ends and the winner should be identified.
        """
        deck_game = Game()
        deck_game.player_1 = Player('Nikos')
        deck_game.player_pc = Player('Computer')
        self.assertTrue(deck_game.check_winner(),\
            'False expected. Players\' health > 0 and central.active.size() = 0')

    def tearDown(self):
        """
        Resets stdout
        """
        sys.stdout = self.actualstdout
        
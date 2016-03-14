import sys
import StringIO
import unittest

from deckgame.helper import Player, Card, CardsCollection
from deckgame.game import Game

class MyTest(unittest.TestCase):
    
    def setUp(self):
        # suppress print statements from original code
        self.actualstdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        
    def test_init_central_deck(self):
        dg = Game()
        dg.init_central_deck()
        self.assertEqual(dg.central['deck'].size(), 36)
        
    def test_computer_buys(self):
        dg = Game()
        dg.aggressive = True
        dg.player_1._money = 3
        dg.central['active']._cards = [Card('Archer', 2, 1, 5), Card('Test1', 3, 2, 5), Card('Test2', 0, 3, 2)]
        dg.central['supplement'].push(Card('Archer', 3, 3, 6))
        dg.computer_buys()
        self.assertNotEqual(dg.central['active']._cards[1]._name, 'Test1')
        
    def test_computer_best_buy_aggressive(self):
        dg = Game()
        dg.aggressive = True
        temp_list = [("S", Card('Archer', 2, 1, 2)), (1, Card('Test1', 2, 2, 1)), (3, Card('Test2', 1, 2, 1))]
        dg.computer_best_buy(temp_list)
        self.assertEqual(dg.computer_best_buy(temp_list), 1)
        
    def test_computer_best_buy_acquisative(self):
        dg = Game()
        dg.aggressive = False
        temp_list = [("S", Card('Archer', 3, 1, 5)), (1, Card('Test1', 1, 3, 3)), (3, Card('Test2', 0, 3, 2))]
        dg.computer_best_buy(temp_list)
        self.assertEqual(dg.computer_best_buy(temp_list), 2)
    
    def test_check_winner_player_1(self):
        dg = Game()
        dg.player_1 = Player('Nikos')
        dg.player_PC = Player('Computer')
        dg.player_1._health = 0
        self.assertTrue(dg.check_winner(), 'True expected. Player 1 wins.')

    def test_check_winner_player_PC(self):
        dg = Game()
        dg.player_1 = Player('Nikos')
        dg.player_PC = Player('Computer')
        dg.player_PC._health = 0
        self.assertTrue(dg.check_winner(), 'True expected. Player PC wins.')    
        
    def test_check_no_winner(self):
        dg = Game()
        dg.player_1 = Player('Nikos')
        dg.player_PC = Player('Computer')
        dg.central['active']._cards = [Card('Archer', 3, 1, 5), Card('Test1', 1, 3, 3), Card('Test2', 0, 3, 2)]
        self.assertFalse(dg.check_winner(), 'False expected. Players\' health > 0 and central.active.size() > 0')
        
    def test_check_winner_empty_active(self):
        dg = Game()
        dg.player_1 = Player('Nikos')
        dg.player_PC = Player('Computer')
        self.assertTrue(dg.check_winner(), 'False expected. Players\' health > 0 and central.active.size() = 0')

    def tearDown(self):
        sys.stdout = self.actualstdout
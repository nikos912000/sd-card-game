import sys
import StringIO
import unittest
from mock import patch

from deckgame.helper import Player, Card, CardsCollection
from deckgame.game import Game

class MyTest(unittest.TestCase):
    
    def setUp(self):
        # suppress print statements from original code
        self.actualstdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        
    def test_player_turn1(self):
        dg = Game()
        dg.init_central_deck()
        dg.player_1.init_deck()
        dg.central['active'].push(Card('Archer', 1, 3, 3), 5)
        dg.player_1.hand.push(Card('Archer', 1, 0, 0))
        dg.player_1.hand.push(Card('Archer', 0, 1, 0))
        dg.player_1.hand.push(Card('Archer', 1, 1, 1))
        dg.player_1.hand.push(Card('Archer', 2, 2, 3), 2)
        ds = dg.player_1.deck.size()
        with patch('__builtin__.raw_input', side_effect=['0', '0', 'A', 'P', 'B', '0', 'B', '0', 'A']) as _raw_input:
            dg.player_1_turn()
            self.assertEquals(dg.player_1.hand.size(), 5)
            self.assertEquals(dg.player_1.deck.size(), ds - 5)
            
    def test_aggressive_opponent(self):
        dg = Game()
        with patch('__builtin__.raw_input', side_effect=['b', 'a']) as _raw_input:
            self.assertTrue(dg.get_opponent())

    def test_acquisative_opponent(self):
        dg = Game()
        with patch('__builtin__.raw_input', return_value='q') as _raw_input:
            self.assertFalse(dg.get_opponent())
        
    def test_set_up_game(self):
        dg = Game()
        dg.set_up_game()
        self.assertEqual(dg.player_1.deck.size(), dg.player_pc.deck.size())
        self.assertEqual(dg.player_1.hand.size(), dg.player_1.handsize)
        self.assertEqual(dg.player_pc.hand.size(), dg.player_pc.handsize)
        self.assertGreater(dg.central['deck'].size(), 0)
    
    def test_init_central_deck(self):
        dg = Game()
        dg.init_central_deck()
        self.assertEqual(dg.central['deck'].size(), 36)
        
    def test_buy_supplement(self):
        dg = Game()
        dg.player_1._money = 6
        dg.central['supplement'].push(Card('Archer', 3, 3, 6))
        with patch('__builtin__.raw_input', return_value='S') as _raw_input:
            dg.player_1_buy()
            self.assertEqual(dg.player_1.money, 0)
            self.assertEqual(dg.central['supplement'].size(), 0)
            
    def test_buy_card(self):
        dg = Game()
        dg.player_1._money = 3
        dg.central['active'].push(Card('Archer', 2, 2, 3))
        with patch('__builtin__.raw_input', return_value='0') as _raw_input:
            dg.player_1_buy()
            self.assertEqual(dg.player_1.money, 0)
            self.assertEqual(dg.central['active'].size(), 0)
            
    def test_buy_card_invalid_index(self):
        dg = Game()
        dg.player_1._money = 3
        dg.central['active'].push(Card('Archer', 2, 2, 3))
        with patch('__builtin__.raw_input', side_effect=['1', 'E']) as _raw_input:
            dg.player_1_buy()
            self.assertEqual(dg.player_1.money, 3)
            self.assertEqual(dg.central['active'].size(), 1)

    def test_player_pc_turn(self):
        dg = Game()
        dg.aggressive = True
        dg.set_up_game()
        pc_ds = dg.player_pc.deck.size()
        dg.player_pc_turn()
        self.assertEqual(dg.player_pc.deck.size(), pc_ds - 5)

    def test_computer_buys(self):
        dg = Game()
        dg.aggressive = True
        dg.player_pc._money = 3
        dg.central['active'].push(Card('Archer', 2, 2, 3))
        dg.central['active'].push(Card('Test1', 3, 1, 3))
        dg.central['active'].push(Card('Test2', 0, 4, 3))
        dg.central['supplement'].push(Card('Archer', 3, 3, 6))
        dg.computer_buy()
        self.assertEqual(dg.player_pc.discard.cards[0].name, 'Test1')
        
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
        dg.player_pc = Player('Computer')
        dg.player_1_health = 0
        self.assertTrue(dg.check_winner(), 'True expected. Player 1 wins.')

    def test_check_winner_player_pc(self):
        dg = Game()
        dg.player_1 = Player('Nikos')
        dg.player_pc = Player('Computer')
        dg.player_pc._health = 0
        self.assertTrue(dg.check_winner(), 'True expected. Player PC wins.')    
        
    def test_check_no_winner(self):
        dg = Game()
        dg.player_1 = Player('Nikos')
        dg.player_pc = Player('Computer')
        dg.central['active']._cards = [Card('Archer', 3, 1, 5), Card('Test1', 1, 3, 3), Card('Test2', 0, 3, 2)]
        self.assertFalse(dg.check_winner(), 'False expected. Players\' health > 0 and central.active.size() > 0')

    def test_check_winner_empty_active(self):
        dg = Game()
        dg.player_1 = Player('Nikos')
        dg.player_pc = Player('Computer')
        self.assertTrue(dg.check_winner(), 'False expected. Players\' health > 0 and central.active.size() = 0')

    def tearDown(self):
        sys.stdout = self.actualstdout
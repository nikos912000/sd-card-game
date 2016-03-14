import sys
import StringIO
import unittest

from deckgame.helper import Player, Card, CardsCollection

class MyTest(unittest.TestCase):
    
    def setUp(self):
        # suppress print statements from original code
        self.actualstdout = sys.stdout
        sys.stdout = StringIO.StringIO()
    
    def test_player_init_(self):
        player = Player('Nikos', health = 20, handsize=3)
        self.assertEqual(player._name, 'Nikos')
        self.assertEqual(player._health, 20)
        self.assertEqual(player._handsize, 3)
    
    def test_player_init_deck(self):
        player = Player('Nikos')
        player.init_deck()
        self.assertEqual(player._deck._cards[0]._name, 'Serf')
        
    def test_player_init_hand(self):
        player = Player('Nikos')
        player.init_deck()
        player.init_hand()
        self.assertEqual(len(player._hand._cards), 5)
        
    def test_player_play_all(self):
        player = Player('Nikos', health = 20, handsize=5)
        player.init_deck()
        player.init_hand()
        player.play_all()
        self.assertEqual(len(player._hand._cards), 0)
        self.assertEqual(len(player._active._cards), 5)
        
    def test_player_play_card(self):
        player = Player('Nikos')
        player.init_deck()
        player.init_hand()
        player.play_card(0)
        self.assertEqual(len(player._hand._cards), 4)
        self.assertEqual(len(player._active._cards), 1)
        player.play_card(6)
        self.assertEqual(len(player._hand._cards), 4)
        self.assertEqual(len(player._active._cards), 1)
        
    def test_player_attack_opponent(self):
        player_1 = Player('Nikos', health = 30)
        player_PC = Player('Computer', health = 30)
        player_1._attack = 5
        player_1.attack_opponent(player_PC)
        self.assertEqual(player_PC._health, 25)
        self.assertEqual(player_1._attack, 0)
    
    def test_player_buy_supplement(self):
        player = Player('Nikos')
        player._money = 2
        central = {'deck': CardsCollection(), 'active': CardsCollection(), 'supplement': CardsCollection(), 'active_size': 5}
        central['supplement'].push(Card('Levy', 1, 2, 2), 10)
        player.buy_supplement(central)
        self.assertEqual(len(central['supplement']._cards), 9)
        self.assertEqual(len(player._discard._cards), 1)
        self.assertEqual(player._money, 0)
        
    def test_player_buy_card(self):
        player = Player('Nikos')
        player.money = 10
        central = {'deck': CardsCollection(), 'active': CardsCollection(), 'supplement': CardsCollection(), 'active_size': 5}
        central['deck'].push(Card('Deck card', 3, 0, 2), 1)
        central['active'].push(Card('Archer', 3, 0, 2), 5)
        player.buy_card(central, 0)
        self.assertEqual(len(central['active']._cards), 5)
        self.assertEqual(len(player._discard._cards), 1)
        self.assertEqual(player._discard._cards[0]._name, 'Archer')
        self.assertEqual(central['active']._cards[4]._name, 'Deck card')
        player.buy_card(central, 0)
        # deck size = 0 now -> no more cards from deck to active area
        self.assertEqual(len(central['active']._cards), 4)
        self.assertEqual(len(player._discard._cards), 2)
        
    def test_player_end_turn(self):
        # checks end turn with 0 cards in player's deck
        # discard pile is shuffled and its cards go to deck
        # new hand with handsize cards is generated from deck
        player = Player('Nikos', handsize = 5)
        player._discard.push(Card('Archer', 3, 0, 2), 10)
        player._active.push(Card('Archer', 3, 0, 2), 4)
        player.end_turn()
        self.assertEqual(len(player._active._cards), 0)
        self.assertEqual(len(player._discard._cards), 0)
        self.assertEqual(len(player._deck._cards), 9)
        self.assertEqual(len(player._hand._cards), 5)
        
    def tearDown(self):
        sys.stdout = self.actualstdout
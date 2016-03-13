import sys
import StringIO

"""
Testing the game
"""

import unittest
from dbc import Player, Central, Card, CardsCollection, DeckGame

class MyTest(unittest.TestCase):
    
    def setUp(self):
        # suppress print statements from original code
        self.actualstdout = sys.stdout
        sys.stdout = StringIO.StringIO()
    
    def test_player_init_(self):
        player = Player('Nikos', health = 20, handsize=3)
        self.assertEqual(player.name, 'Nikos')
        self.assertEqual(player.health, 20)
        self.assertEqual(player.handsize, 3)
    
    def test_player_init_deck(self):
        player = Player('Nikos')
        player.init_deck()
        self.assertEqual(player.deck.cards[0].name, 'Serf')
        
    def test_player_init_hand(self):
        player = Player('Nikos')
        player.init_deck()
        player.init_hand()
        self.assertEqual(len(player.hand.cards), 5)
        
    def test_player_play_all(self):
        player = Player('Nikos', health = 20, handsize=5)
        player.init_deck()
        player.init_hand()
        player.play_all()
        self.assertEqual(len(player.hand.cards), 0)
        self.assertEqual(len(player.active.cards), 5)
        
    def test_player_play_card(self):
        player = Player('Nikos')
        player.init_deck()
        player.init_hand()
        player.play_card(0)
        self.assertEqual(len(player.hand.cards), 4)
        self.assertEqual(len(player.active.cards), 1)
        player.play_card(6)
        self.assertEqual(len(player.hand.cards), 4)
        self.assertEqual(len(player.active.cards), 1)
        
    def test_player_attack_opponent(self):
        player_1 = Player('Nikos', health = 30)
        player_PC = Player('Computer', health = 30)
        player_1.attack = 5
        player_1.attack_opponent(player_PC)
        self.assertEqual(player_PC.health, 25)
        self.assertEqual(player_1.attack, 0)
    
    def test_player_buy_supplement(self):
        player = Player('Nikos')
        player.money = 2
        central = Central()
        central.supplement.push(Card('Levy', 1, 2, 2), 10)
        player.buy_supplement(central)
        self.assertEqual(len(central.supplement.cards), 9)
        self.assertEqual(len(player.discard.cards), 1)
        self.assertEqual(player.money, 0)
        
    def test_player_buy_card(self):
        player = Player('Nikos')
        player.money = 10
        central = Central()
        central.deck.push(Card('Deck card', 3, 0, 2), 1)
        central.active.push(Card('Archer', 3, 0, 2), 5)
        player.buy_card(central, 0)
        self.assertEqual(len(central.active.cards), 5)
        self.assertEqual(len(player.discard.cards), 1)
        self.assertEqual(player.discard.cards[0].name, 'Archer')
        self.assertEqual(central.active.cards[4].name, 'Deck card')
        player.buy_card(central, 0)
        # deck size = 0 now -> no more cards from deck to active area
        self.assertEqual(len(central.active.cards), 4)
        self.assertEqual(len(player.discard.cards), 2)
        
    def test_player_end_turn(self):
        # checks end turn with 0 cards in player's deck
        # discard pile is shuffled and its cards go to deck
        # new hand with handsize cards is generated from deck
        player = Player('Nikos', handsize = 5)
        player.discard.push(Card('Archer', 3, 0, 2), 10)
        player.active.push(Card('Archer', 3, 0, 2), 4)
        player.end_turn()
        self.assertEqual(len(player.active.cards), 0)
        self.assertEqual(len(player.discard.cards), 0)
        self.assertEqual(len(player.deck.cards), 9)
        self.assertEqual(len(player.hand.cards), 5)
        
    def tet_card_init_(self):
        card = Card('Levy', 1, 2, 2)
        self.assertEqual(card.name, 'Levy')
        self.assertEqual(card.attack, 1)
        self.assertEqual(card.money, 2)
        self.assertEqual(card.cost, 2)
        
    def test_central_init(self):
        central = Central()
        self.assertEqual(central.activeSize, 5)
        self.assertEqual(central.active.cards, [])
        self.assertEqual(central.deck.cards, [])
        self.assertEqual(central.supplement.cards, [])
        
    def test_collection_shuffle(self):
        collection = CardsCollection()
        collection.push(Card('Archer', 3, 0, 2), 5)
        collection.push(Card('Deck card', 3, 0, 2), 5)
        collection.shuffle_collection()
        self.assertEqual(len(collection.cards), 10)
        
    def test_collection_clear(self):
        collection = CardsCollection()
        collection.push(Card('Archer', 3, 0, 2), 5)
        collection.push(Card('Deck card', 3, 0, 2), 5)
        collection.clear_collection()
        self.assertEqual(collection.cards, [])
        
    def test_collection_replace(self):
        collection1 = CardsCollection()
        collection2 = CardsCollection()
        collection1.push(Card('Archer', 3, 0, 2), 2)
        collection2.push(Card('Deck card', 3, 0, 2), 3)
        collection1.replace(collection2)
        self.assertEqual(collection1.cards, collection2.cards)
        
    def test_collection_push(self):
        collection = CardsCollection()
        card1 = Card('Archer', 3, 0, 2)
        card2 = Card('Archer', 1, 2, 1)
        collection.push(card1, 2)
        collection.push(card2)
        temp_list = [card1, card1, card2]
        self.assertSequenceEqual(collection.cards, temp_list)
        
    def test_collection_pop(self):
        collection = CardsCollection()
        card1 = Card('Archer', 3, 0, 2)
        card2 = Card('Test1', 1, 1, 1)
        card3 = Card('Test2', 1, 2, 1)
        collection.push(card1, 1)
        collection.push(card2, 2)
        collection.push(card3, 1)
        card_pop = collection.pop()
        self.assertEqual(card_pop, card3)
        card_pop = collection.pop(0)
        self.assertEqual(card_pop, card1)
        
    def test_collection_size(self):
        collection = CardsCollection()
        self.assertEqual(collection.size(), 0)
        collection.push(Card('Archer', 3, 0, 5), 2)
        collection.push(Card('Test1', 1, 1, 1), 3)
        self.assertEqual(collection.size(), 5)
        
    def test_computer_best_buy_aggressive(self):
        dg = DeckGame()
        dg.aggressive = True
        temp_list = [("S", Card('Archer', 2, 1, 2)), (1, Card('Test1', 2, 2, 1)), (3, Card('Test2', 1, 2, 1))]
        dg.computer_best_buy(temp_list)
        self.assertEqual(dg.computer_best_buy(temp_list), 1)
        
    def test_computer_best_buy_acquisative(self):
        dg = DeckGame()
        dg.aggressive = False
        temp_list = [("S", Card('Archer', 3, 1, 5)), (1, Card('Test1', 1, 3, 3)), (3, Card('Test2', 0, 3, 2))]
        dg.computer_best_buy(temp_list)
        self.assertEqual(dg.computer_best_buy(temp_list), 2)
    
    

    def tearDown(self):
        sys.stdout = self.actualstdout
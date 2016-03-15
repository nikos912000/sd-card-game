import sys
import StringIO
import unittest

from deckgame.helper import Card

class MyTest(unittest.TestCase):
    
    def setUp(self):
        # suppress print statements from original code
        self.actualstdout = sys.stdout
        sys.stdout = StringIO.StringIO()
    
    def test_init_(self):
        card = Card('Archer', 3, 0, 2)
        self.assertEqual(card.name, 'Archer')
        self.assertEqual(card.attack, 3)
        self.assertEqual(card.money, 0)
        self.assertEqual(card.cost, 2)

    def test_init_default_values(self):
        card = Card('Archer')
        self.assertEqual(card.name, 'Archer')
        self.assertEqual(card.attack, 0)
        self.assertEqual(card.money, 0)
        self.assertEqual(card.cost, 0)

    def test_init_default_attack(self):
        card = Card('Archer', money = 1, cost = 1)
        self.assertEqual(card.name, 'Archer')
        self.assertEqual(card.attack, 0)
        self.assertEqual(card.money, 1)
        self.assertEqual(card.cost, 1)

    def tearDown(self):
        sys.stdout = self.actualstdout
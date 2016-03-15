"""
Testing the Card class.
"""

import sys
import StringIO
import unittest

from deckgame.helper import Card


class MyTest(unittest.TestCase):
    """
    Tests for the Card class.
    """
    def setUp(self):
        """
        Suppresses print statements from original code.
        """
        self.actualstdout = sys.stdout
        sys.stdout = StringIO.StringIO()

    def test_init_(self):
        """
        Tests the initialiser of the class in case of non-default parameters.
        """
        card = Card('Archer', 3, 0, 2)
        self.assertEqual(card.name, 'Archer')
        self.assertEqual(card.attack, 3)
        self.assertEqual(card.money, 0)
        self.assertEqual(card.cost, 2)

    def test_init_default_values(self):
        """
        Tests the initialiser of the class in case of default parameters.
        """
        card = Card('Archer')
        self.assertEqual(card.name, 'Archer')
        self.assertEqual(card.attack, 0)
        self.assertEqual(card.money, 0)
        self.assertEqual(card.cost, 0)

    def test_init_default_attack(self):
        """
        Tests the initialiser of the class in case of default and non-default
        parameters.
        """
        card = Card('Archer', money=1, cost=1)
        self.assertEqual(card.name, 'Archer')
        self.assertEqual(card.attack, 0)
        self.assertEqual(card.money, 1)
        self.assertEqual(card.cost, 1)

    def tearDown(self):
        """
        Resets stdout
        """
        sys.stdout = self.actualstdout

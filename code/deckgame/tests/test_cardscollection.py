"""
Testing the CardsCollection class.
"""

import sys
import StringIO
import unittest

from deckgame.helper import Card, CardsCollection

class MyTest(unittest.TestCase):
    """
    Tests for the CardsCollection class.
    """
    def setUp(self):
        """
        Suppresses print statements from original code.
        """
        self.actualstdout = sys.stdout
        sys.stdout = StringIO.StringIO()

    def test_collection_shuffle(self):
        """
        Tests whether the shuffling results to unexpected results.
        """
        collection = CardsCollection()
        collection.push(Card('Archer', 3, 0, 2), 5)
        collection.push(Card('Deck card', 3, 0, 2), 5)
        collection.shuffle_collection()
        self.assertEqual(len(collection.cards), 10)

    def test_collection_clear(self):
        """
        Tests whether the list is cleared when using the appropriate method.
        """
        collection = CardsCollection()
        collection.push(Card('Archer', 3, 0, 2), 5)
        collection.push(Card('Deck card', 3, 0, 2), 5)
        collection.clear_collection()
        self.assertEqual(collection.cards, [])

    def test_collection_replace(self):
        """
        Tests whether collection's content is correctly replaced by that of
        another -given- collection, when calling the appropriate method.
        """
        collection1 = CardsCollection()
        collection2 = CardsCollection()
        collection1.push(Card('Archer', 3, 0, 2), 2)
        collection2.push(Card('Deck card', 3, 0, 2), 3)
        collection1.replace(collection2)
        self.assertEqual(collection1.cards, collection2.cards)

    def test_collection_push(self):
        """
        Tests whether cards are appended successfully and correctly to the
        list.
        """
        collection = CardsCollection()
        card1 = Card('Archer', 3, 0, 2)
        card2 = Card('Archer', 1, 2, 1)
        collection.push(card1, 2)
        collection.push(card2)
        temp_list = [card1, card1, card2]
        self.assertSequenceEqual(collection.cards, temp_list)

    def test_collection_pop(self):
        """
        Tests whether cards are removed successfully and correctly by the
        list.
        """
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
        """
        Tests whether the size of the list returned when calling the
        appropriate method is the expected one.
        """
        collection = CardsCollection()
        self.assertEqual(collection.size(), 0)
        collection.push(Card('Archer', 3, 0, 5), 2)
        collection.push(Card('Test1', 1, 1, 1), 3)
        self.assertEqual(collection.size(), 5)

    def tearDown(self):
        """
        Resets stdout
        """
        sys.stdout = self.actualstdout

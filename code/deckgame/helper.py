import random


class Player(object):
    def __init__(self, name, health = 30, handsize = 5):
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
        return self._name
    
    @property
    def health(self):
        return self._health
    
    @property
    def handsize(self):
        return self._handsize
    
    @property
    def strength(self):
        return self._strength
    
    @property
    def money(self):
        return self._money
    
    @property
    def attack(self):
        return self._attack

    @property
    def deck(self):
        return self._deck
    
    @property
    def hand(self):
        return self._hand
    
    @property
    def active(self):
        return self._active
    
    @property
    def discard(self):
        return self._discard

    def init_hand(self):
        for _ in range(self._handsize):
            if self._deck.size() == 0:
                self._discard.shuffle_collection()
                self._deck.replace(self._discard)
                self._discard.clear_collection()
            card = self._deck.pop()
            self._hand.push(card)
    
    def init_deck(self):
        self._deck.push(Card('Serf', 0, 1, 0), 8)
        self._deck.push(Card('Squire', 1, 0, 0), 2)
        
    def play_all(self):
        for _ in range(self._hand.size()):
            card = self._hand.pop()
            self._active.push(card)
            self._money = self._money + card._money
            self._attack = self._attack + card._attack
        print '\nPlayed all cards!'
            
    def play_card(self, index):
        if index < self._hand.size():
            card = self._hand.pop(index)
            self._active.push(card)
            self._money = self._money + card._money
            self._attack = self._attack + card._attack
            print '\nCard played:\n%s' % card
        else:
            print "\nInvalid index number! Please type a valid number!" 
                
    def attack_opponent(self, opponent):
        opponent._health = opponent._health - self._attack
        self._attack = 0
        
    def buy_supplement(self, central):
        self._money = self._money - central['supplement']._cards[0]._cost
        card = central['supplement'].pop()
        self._discard.push(card)
        self._strength = self._strength + card._attack
        print "\nSupplement bought:\n%s" % card
        
    def buy_card(self, central, index):
        self._money = self._money - central['active']._cards[index]._cost
        card = central['active'].pop(index)
        self._discard.push(card)
        self._strength = self._strength + card._attack
        print "\nCard bought:\n%s" % card
        
        if central['deck'].size() > 0:
            card = central['deck'].pop()
            central['active'].push(card)
                
    def end_turn(self):
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
                
    def print_values(self):
        print "Money %s, Attack %s" % (self._money, self._attack)
    
    def compute_strength(self):
        for card in self._deck._cards:
            self._strength = self._strength + card._attack 

class Card(object):
    def __init__(self, name, attack = 0, money = 0, cost = 0):
        self._name = name
        self._money = money
        self._attack = attack
        self._cost = cost      
    
    @property
    def name(self):
        return self._name
    
    @property
    def money(self):
        return self._money
    
    @property
    def attack(self):
        return self._attack
    
    @property
    def cost(self):
        return self._cost
    
    def __str__(self):
        return 'Name: %s, costing %s with attack %s and money %s' % (self._name, self._cost, self._attack, self._money)
  
class CardsCollection():
    def __init__(self):
        self._cards = []
        
    @property
    def cards(self):
        return self._cards
        
    def shuffle_collection(self):
        random.shuffle(self._cards)    
    
    def clear_collection(self):
        self._cards = []
    
    def replace(self, collection):
        self._cards = collection._cards
        
    def push(self, card, times = 1):
        self._cards.extend(times * [card])
        
    def pop(self, i = -1):
        return self._cards.pop(i)
        
    def size(self):
        return len(self._cards)
    
    def print_collection(self, index = False):
        if index:
            for i in range(self.size()):
                print "[%s] %s" % (i, self._cards[i])
        else:
            for i in range(self.size()):
                print self._cards[i]

    def print_card(self, idx = 0):
        print self._cards[idx]

    
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()

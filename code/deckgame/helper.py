import random


class Player(object):
    def __init__(self, name, health = 30, handsize = 5):
        self.name = name
        self.health = health
        self.handsize = handsize
        self.strength = 0
        self.money = 0
        self.attack = 0
        self.deck = CardsCollection()
        self.hand = CardsCollection()
        self.active = CardsCollection()
        self.discard = CardsCollection()

    def init_hand(self):
        for _ in range(self.handsize):
            if self.deck.size() == 0:
                self.discard.shuffle_collection()
                self.deck.replace(self.discard)
                self.discard.clear_collection()
            card = self.deck.pop()
            self.hand.push(card)
    
    def init_deck(self):
        self.deck.push(Card('Serf', 0, 1, 0), 8)
        self.deck.push(Card('Squire', 1, 0, 0), 2)
        
    def play_all(self):
        for _ in range(self.hand.size()):
            card = self.hand.pop()
            self.active.push(card)
            self.money = self.money + card.money
            self.attack = self.attack + card.attack
        print '\nPlayed all cards!'
            
    def play_card(self, index):
        if( index < self.hand.size()):
            card = self.hand.pop(index)
            self.active.push(card)
            self.money = self.money + card.money
            self.attack = self.attack + card.attack
            print '\nCard played:\n%s' % card
        else:
            print "\nInvalid index number! Please type a valid number!" 
                
    def attack_opponent(self, opponent):
        opponent.health = opponent.health - self.attack
        self.attack = 0
        
    def buy_supplement(self, central):
        self.money = self.money - central.supplement.cards[0].cost
        card = central.supplement.pop()
        self.discard.push(card)
        self.strength = self.strength + card.attack
        print "\nSupplement bought:\n%s" % card
        
    def buy_card(self, central, index):
        self.money = self.money - central.active.cards[index].cost
        card = central.active.pop(index)
        self.discard.push(card)
        self.strength = self.strength + card.attack
        print "\nCard bought:\n%s" % card
        
        if central.deck.size() > 0:
            card = central.deck.pop()
            central.active.push(card)
                
    def end_turn(self):
        for _ in range(self.hand.size()):
            card = self.hand.pop()
            self.discard.push(card)

        for _ in range(self.active.size()):
            card = self.active.pop()
            self.discard.push(card)
                
        for _ in range(self.handsize):
            if self.deck.size() == 0:
                self.discard.shuffle_collection()
                self.deck.replace(self.discard)
                self.discard.clear_collection()
            card = self.deck.pop()
            self.hand.push(card)
                
    def print_values(self):
        print "Money %s, Attack %s" % (self.money, self.attack)
    
    def compute_strength(self):
        for card in self.deck.cards:
            self.strength = self.strength + card.attack 

class Card(object):
    def __init__(self, name, attack = 0, money = 0, cost = 0):
        self.name = name
        self.money = money
        self.attack = attack
        self.cost = cost      
        
    def __str__(self):
        return 'Name: %s, costing %s with attack %s and money %s' % (self.name, self.cost, self.attack, self.money)
        
class Central(object):
    def __init__(self, activeSize = 5):
        self.activeSize = activeSize
        self.active = CardsCollection()
        self.deck = CardsCollection()
        self.supplement = CardsCollection()
  
class CardsCollection():
    def __init__(self):
        self.cards = []
        
    def shuffle_collection(self):
        random.shuffle(self.cards)    
    
    def clear_collection(self):
        self.cards = []
    
    def replace(self, collection):
        self.cards = collection.cards
        
    def push(self, card, times = 1):
        self.cards.extend(times * [card])
        
    def pop(self, i=-1):
        return self.cards.pop(i)
        
    def size(self):
        return len(self.cards)
    
    def print_collection(self, index = False):
        if index:
            for i in range(self.size()):
                print "[%s] %s" % (i, self.cards[i])
        else:
            for i in range(self.size()):
                print self.cards[i]

    def print_card(self, idx = 0):
        print self.cards[idx]

    
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

import itertools
import random

class Player(object):
    def __init__(self, name, health = 30, handsize = 5):
        self.name = name
        self.health = health
        self.handsize = handsize
        self.money = 0
        self.attack = 0
        self.deck = CardsCollection()
        self.hand = CardsCollection()
        self.active = CardsCollection()
        self.discard = CardsCollection()

    def init_hand(self):
        for x in range(self.handsize):
            if self.deck.size == 0:
                self.discard.shuffle_collection()
                self.deck.replace(self.discard)
                self.discard.clear_collection()
            card = self.deck.pop()
            self.hand.push(card)
    
    def init_deck(self):
        self.deck.push(Card('Serf', 0, 1, 0), 8)
        self.deck.push(Card('Squire', 1, 0, 0), 2)
        
    def play_all(self):
        for x in range(self.hand.size()):
            card = self.hand.pop()
            self.active.push(card)
            self.money = self.money + card.money
            self.attack = self.attack + card.attack
            
    def play_card(self, index):
        if( index < self.hand.size()):
            card = self.hand.pop(index)
            self.active.push(card)
            for card in self.active.cards:
                self.money = self.money + card.money
                self.attack = self.attack + card.attack
                
    def end_turn(self):
        for x in range(self.hand.size()):
            card = self.hand.pop()
            self.discard.push(card)

        for x in range(self.active.size()):
            card = self.active.pop()
            self.discard.push(card)
                
        for x in range(self.handsize):
            if self.deck.size() == 0:
                self.discard.shuffle_collection()
                self.deck.replace(self.discard)
                self.discard.clear_collection()
            card = self.deck.pop()
            self.hand.push(card)
                
    def print_values(self):
        print "Money %s, Attack %s" % (self.money, self.attack)
    
    def print_health(self):
        print "\n" + self.name + " Health %s" % self.health

class Card(object):
    def __init__(self, name, attack = 0, money = 0, cost = 1):
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
    
  
class DeckGame():
    def __init__(self):
        self.player_1 = Player('Player 1')
        self.player_PC = Player('Player PC')
        self.central = Central()
        
    def start_game(self):
        while True:
            opponent = raw_input("Do you want an aggressive (A) opponent or an acquisative (Q) opponent")
            if opponent.lower() =='a':
                self.aggressive = True
                break
            elif opponent.lower() =='q':
                self.aggressive = False
                break
            else:
                print 'Please give a valid option!'
        
        self.set_up_game()

        winner = False
        while not winner:
            while True:
    
                print "\nPlayer Health: %s" % self.player_1.health
                print "Computer Health: %s" % self.player_PC.health
    
                print "\nYour Hand:"
                self.player_1.hand.print_collection(index = True)
                print "\nYour Values:"
                self.player_1.print_values()
    
                print "\nChoose Action: (P = play all, [0-n] = play that card, B = Buy Card, A = Attack, E = end turn)"
    
                act = raw_input("Enter Action: ")
                if act == 'P':
                    self.player_1.play_all()
                    print "\nYour Hand:"
                    self.player_1.hand.print_collection(index = True)
                    print "\nYour Active Cards:"
                    self.player_1.active.print_collection()
                    print "\nYour Values:"
                    self.player_1.print_values()
                elif act.isdigit():
                    index = int(act)
                    self.player_1.play_card(index)
                    print "\nYour Hand"
                    self.player_1.hand.print_collection(index = True)
            
                    print "\nYour Active Cards"
                    self.player_1.active.print_collection()
                    print "\nYour Values"
                    self.player_1.print_values()
                elif (act == 'B'):
                    self.buy()
                elif act == 'A':
                    self.attack()
                elif act == 'E':
                    self.end_turn()
                    break
                else:
                    print "\n Please give a valid option"
                    
            print "Available Cards to buy:"
            self.central.active.print_collection()
        
            print "Supplement:"
            if self.central.supplement.size > 0:
                print self.central.supplement.print_card(0)
    
            self.player_1.print_health()
            self.player_PC.print_health()
    
            self.player_PC.play_all()
    
            print " Computer player values attack %s, money %s" % (self.player_PC.attack, self.player_PC.money)
            print " Computer attacking with strength %s" % self.player_PC.attack
            self.player_1.health = self.player_1.health - self.player_PC.attack
            self.player_PC.attack = 0
            
            self.player_1.print_health()
            self.player_PC.print_health()
            print " Computer player values attack %s, money %s" % (self.player_PC.attack, self.player_PC.money)
            print "Computer buying"
            
            self.computer_plays()
            
            print "Available Cards to buy:"
            self.central.active.print_collection()
        
            print "Supplement:"
            if self.central.supplement.size > 0:
                print self.central.supplement.print_card(0)
    
            self.player_1.print_health()
            self.player_PC.print_health()
            
            winner = self.check_winner()
        return
            
    def set_up_game(self):
        
        self.init_central_deck()
        self.init_supplement()
        
        self.central.deck.shuffle_collection()
        for i in range(self.central.activeSize):
            card = self.central.deck.pop()
            self.central.active.push(card)
            
        self.player_1.init_deck()
        self.player_PC.init_deck()    
        
        self.player_1.init_hand()
        self.player_PC.init_hand()
        
        print "\nAvailable Cards to buy:"
        self.central.active.print_collection(index = True)
    
        print "\nSupplement:"
        if self.central.supplement.size > 0:
            self.central.supplement.print_card(0)
    
    def init_central_deck(self):
        self.central.deck.push(Card('Archer', 3, 0, 2), 4)
        self.central.deck.push(Card('Baker', 0, 3, 2), 4)
        self.central.deck.push(Card('Swordsman', 4, 0, 3), 3)
        self.central.deck.push(Card('Knight', 6, 0, 5), 2)
        self.central.deck.push(Card('Tailor', 0, 4, 3), 3)
        self.central.deck.push(Card('Crossbowman', 4, 0, 3), 3)
        self.central.deck.push(Card('Merchant', 0, 5, 4), 3)
        self.central.deck.push(Card('Thug', 2, 0, 1), 4)
        self.central.deck.push(Card('Thief', 1, 1, 1), 4)
        self.central.deck.push(Card('Catapault', 7, 0, 6), 2)
        self.central.deck.push(Card('Caravan', 1, 5, 5), 2)
        self.central.deck.push(Card('Assassin', 5, 0, 4), 2)    
  
    def init_supplement(self):
        self.central.supplement.push(Card('Levy', 1, 2, 2), 10)

    def buy(self):
        notending = True
        while self.player1.money > 0:
            print "Available Cards"
            self.central.active.print_collection(indexes = True)
            
            print "Choose a card to buy [0-n], S for supplement, E to end buying"
            buy_choice = raw_input("Choose option: ")
            if buy_choice == 'S':
                self.buy_supplement()
            elif buy_choice == 'E':
                notending = False
                break
            elif buy_choice.isdigit():
                self.buy_card(int(buy_choice))
            else:
                print "Enter a valid option"
     
    def buy_supplement(self):
        if self.central.supplemment.size() > 0:
            if self.player1.money > self.central.supplement.cards[0].cost:
                self.player1.money = self.player1.money - self.central.supplement.cards[0].cost
                card = self.central.supplement.pop()
                self.player1.discard.push(card)
                print "Supplement Bought"
            else:
                print "insufficient money to buy"
        else:
            print "no supplements left"
            
    def buy_card(self, index):
        if index < self.central.active.size():
            if self.player1.money >= self.central.active.cards[index].cost:
                self.player1.money = self.player1.money - self.central.active.cards[index].cost
                card = self.central.active.pop(index)
                self.player1.discard.push(card)
                
                if self.central.deck.size() > 0:
                    card = self.central.deck.pop()
                    self.central.active.push(card)
                else:
                    self.central.activeSize = self.central.activeSize - 1
                print "Card bought"
            else:
                print "insufficient money to buy"
        else:
            print "enter a valid index number"
                
    def attack(self):
        self.player_PC.health = self.player_PC.health - self.player_1.attack
        self.player1.attack = 0
    
    def computer_plays(self):
        if self.player_PC.money > 0:
            cb = True
            templist = []
            print "Starting Money %s" % self.player_PC.money
            while cb:
                templist = []
                if self.central.supplement.size() > 0:
                    card  = self.central.supplement.cards[0]
                    if card.cost <= self.player_PC.money:
                        templist.append(("S", card))
                for i in range(self.central.activeSize):
                    card = self.central.active.cards[i]
                    if card.cost <= self.player_PC.money:
                        templist.append((i, card))
                if len(templist) > 0:
                    highest_idx = 0
                    
                    for current_idx in range(len(templist)):
                        if templist[current_idx][1].cost > templist[highest_idx][1].cost:
                            highest_idx = current_idx
                        if templist[current_idx][1].cost == templist[highest_idx][1].cost:
                            if self.aggressive:
                                if templist[current_idx][1].get_attack() > templist[highest_idx][1].attack:
                                    highest_idx = current_idx
                            else:
                                if templist[current_idx][1].money > templist[highest_idx][1].money:
                                    highest_idx = current_idx
                                    
                    #if "S"?
                    source = templist[highest_idx][0]
                    if source in range(self.central.activeSize):
                        index = int(source)
                        card = self.central.active.cards[index]
                        if self.player_PC.money >= card.cost:
                            self.player_PC.money = self.player_PC.money - card.cost
                            card = self.central.active.pop(index)
                            print "Card bought %s" % card
                            self.player_PC.discard.push(card)
                            if self.central.deck.size() > 0:
                                card = self.central.deck.pop()
                                self.central.deck.push(card)
                            else:
                                self.central.activeSize = self.central.activeSize - 1
                        else:
                            print "Error Occurred"
                    else:
                        card = self.central.supplement.cards[0]
                        if self.player_PC.money >= card.cost:
                            self.player_PC.money = self.player_PC.money - card.cost
                            card = self.central.supplement.pop()
                            self.player_PC.discard.push(card)
                            print "Supplement Bought %s" % card
                        else:
                            print "Error Occurred"
                else:
                    cb = False
                if self.player_PC == 0:
                    cb = False
        else:
            print "No Money to buy anything"

        self.end_turn(self.player_PC)
                    
        print "Computer turn ending"
        
    def check_winner(self):
        winner = False
        if self.player_1.health <= 0:
            winner = True
            print "Computer wins"
        elif self.player_PC.health <= 0:
            winner = True
            print 'Player One Wins'
        elif self.central.activeSize == 0:
            print "No more cards available"
            if self.player_1.health > self.player_PC.health:
                print "Player One Wins on Health"
            elif self.player_PC.health > self.player_1.health:
                print "Computer Wins"
            else:
                pHT = 0
                pCT = 0
                if self.player_1.attack > self.player_PC.attack:
                    print "Player One Wins on Card Strength"
                elif self.player_PC.attack > self.player_1.attack:
                    print "Computer Wins on Card Strength"
                else:
                    print "Draw"
            winner = True
        return winner
  
if __name__ == '__main__':

    while True:
        pG = raw_input('Do you want to play a game?:')
        if pG.lower() =='y':
            new_game = True
        elif pG.lower() =='n':
            new_game = False
        else:
            print 'Please give a valid option!'
            continue
        if new_game:
            game = DeckGame()
            game.start_game()
        else:
            break

    exit()

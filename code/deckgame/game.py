from helper import Player, CardsCollection, Card

class Game():
    def __init__(self):
        self.player_1 = Player('Player 1')
        self.player_PC = Player('Player PC')
        self.central = {'deck': CardsCollection(), 'active': CardsCollection(), 'supplement': CardsCollection(), 'active_size': 5}
   
    def start_game(self):
        self.aggressive = self.get_opponent()
        self.set_up_game()

        winner = False
        while not winner:
            self.player_1_turn()
            self.display_info()
            self.player_PC_turn()
            self.display_info()
            winner = self.check_winner()
        return
    
    def get_opponent(self):
        while True:
            opponent = raw_input("Do you want an aggressive (A) or an acquisative (Q) opponent?")
            if opponent.lower() =='a':
                print 'Playing against aggressive opponent'
                return True
            elif opponent.lower() =='q':
                print 'Playing against acquisative opponent'
                return False
            # check cancel
            else:
                print 'Please give a valid option!'
            
    def set_up_game(self):
        self.init_central_deck()
        self.init_supplement()
        
        self.central['deck'].shuffle_collection()
        for _ in range(self.central['active_size']):
            card = self.central['deck'].pop()
            self.central['active'].push(card)
            
        self.player_1.init_deck()
        self.player_PC.init_deck()
        
        self.player_1.compute_strength()
        self.player_PC.compute_strength()
        
        self.player_1.init_hand()
        self.player_PC.init_hand()
    
    def init_central_deck(self):
        self.central['deck'].push(Card('Archer', 3, 0, 2), 4)
        self.central['deck'].push(Card('Baker', 0, 3, 2), 4)
        self.central['deck'].push(Card('Swordsman', 4, 0, 3), 3)
        self.central['deck'].push(Card('Knight', 6, 0, 5), 2)
        self.central['deck'].push(Card('Tailor', 0, 4, 3), 3)
        self.central['deck'].push(Card('Crossbowman', 4, 0, 3), 3)
        self.central['deck'].push(Card('Merchant', 0, 5, 4), 3)
        self.central['deck'].push(Card('Thug', 2, 0, 1), 4)
        self.central['deck'].push(Card('Thief', 1, 1, 1), 4)
        self.central['deck'].push(Card('Catapault', 7, 0, 6), 2)
        self.central['deck'].push(Card('Caravan', 1, 5, 5), 2)
        self.central['deck'].push(Card('Assassin', 5, 0, 4), 2)    
  
    def init_supplement(self):
        self.central['supplement'].push(Card('Levy', 1, 2, 2), 10)
        
    def display_info(self):
        print '\n|----------------------------------------|'
        print '|----------------- INFO -----------------|'
        print '|----------------------------------------|'
        print 'Health:'
        print 'You: %s' % self.player_1._health
        print 'PC: %s' % self.player_PC._health
        
        print "\nYour Values:"
        self.player_1.print_values()

        print "\nYour Hand:"
        self.player_1._hand.print_collection(index = True)
        
        print "\nYour active area:"
        self.player_1._active.print_collection()
        
        print "\nAvailable Cards to buy:"
        self.central['active'].print_collection(index = True)

        print "\nSupplement:"
        if self.central['supplement'].size() > 0:
            self.central['supplement'].print_card(0)
        
        print '----------------------------------------'
        
    def player_1_turn(self):
        while True:
            self.display_info()
            print '\n----------------------------------------'
            print "Choose Action: (P = play all, [0-n] = play that card, B = Buy Card, A = Attack, E = end turn)"

            action = raw_input("Enter Action: ")
            if action == 'P':
                if self.player_1._hand.size() > 0:
                    self.player_1.play_all()
                else:
                    print '\nNo more cards to play!\nPlease choose a valid option!'
            elif action.isdigit():
                if self.player_1._hand.size() > 0:
                    index = int(action)
                    self.player_1.play_card(index)
                else:
                    print '\nNo more cards to play!\nPlease choose a valid option!'
            elif (action == 'B'):
                if self.player_1._active.size() > 0:
                    self.buy()
                else:
                    print '\nNo cards in active area! \nPlease play cards!' 
            elif action == 'A':
                if self.player_1._active.size() > 0:
                    self.player_1.attack_opponent(self.player_PC)
                else:
                    print '\nNo cards in active area! \nPlease play cards!' 
            elif action == 'E':
                self.player_1.end_turn()
                break
            else:
                print "\nPlease give a valid option"
            
            if self.player_1._money == 0 and self.player_1._attack == 0 and self.player_1._hand.size() == 0:
                print '\nNo more possible actions.\nTurn ending.'
                self.player_1.end_turn()
                break
            
    def player_PC_turn(self):
        self.player_PC.play_all()
    
        print "\nComputer Values:"
        self.player_PC.print_values()

        print "Computer attacking with strength %s..." % self.player_PC._attack
        self.player_PC.attack_opponent(self.player_1)
        
        print '\nHealth:'
        print 'You: %s' % self.player_1._health
        print 'PC: %s' % self.player_PC._health
        print "\nComputer Values:"
        self.player_PC.print_values()
        
        print "Computer buying..."
        self.computer_buys()
               
        self.player_PC.end_turn()
        print "Computer turn ending"
        
    def buy(self):
        while self.player_1._money > 0:
            print "\nAvailable Cards:"
            self.central['active'].print_collection(index = True)
            
            print "\nSupplement:"
            if self.central['supplement'].size() > 0:
                self.central['supplement'].print_card(0)
                
            print "\nYour Values:"
            self.player_1.print_values()
            
            print '\n----------------------------------------'
            print "Choose a card to buy: ([0-n], S for supplement, E to end buying)"
            buy_choice = raw_input("Choose option: ")
            if buy_choice == 'S':
                if self.central['supplement'].size() > 0:
                    if self.player_1._money >= self.central['supplement']._cards[0]._cost:
                        self.player_1.buy_supplement(self.central)
                    else:
                        print "\nInsufficient money to buy! Please choose another option!"
                else:
                    print "\nNo supplements left!"
                print "\nYour Values:"
                self.player_1.print_values()
            elif buy_choice == 'E':
                break
            elif buy_choice.isdigit():
                index = int(buy_choice)
                if index < self.central['active'].size():
                    if self.player_1._money >= self.central['active']._cards[index]._cost:
                        self.player_1.buy_card(self.central, index)                       
                    else:
                        print "\nInsufficient money to buy! Please choose another option!"
                else:
                    print "\nInvalid index number! Please type a valid number!"
                print "\nYour Values:"
                self.player_1.print_values()
            else:
                print "\nPlease enter a valid option!"
        print '\nNo money left to buy!'
                
    def computer_buys(self):
        if self.player_PC._money > 0:
            templist = []
            print "Starting Money %s" % self.player_PC._money
            while True:
                templist = []
                if self.central['supplement'].size() > 0:
                    card  = self.central['supplement']._cards[0]
                    if self.player_PC._money >= card._cost:
                        templist.append(("S", card))
                for i in range(self.central['active'].size()):
                    card = self.central['active']._cards[i]
                    if self.player_PC._money >= card._cost:
                        templist.append((i, card))
                # check if there are possible cards to buy
                if len(templist) > 0:
                    highest_idx = self.computer_best_buy(templist)

                    source = templist[highest_idx][0]
                    if source in range(self.central['active'].size()):
                        index = int(source)
                        self.player_PC.buy_card(self.central, index)
                    else:
                        self.player_PC.buy_supplement(self.central)
                else:
                    break
                if self.player_PC._money == 0:
                    break
        else:
            print "No Money to buy anything"

    def computer_best_buy(self, templist):
        highest_idx = 0
                    
        for current_idx in range(len(templist)):
            if self.aggressive:
                if templist[current_idx][1]._attack > templist[highest_idx][1]._attack:
                    highest_idx = current_idx
                elif templist[current_idx][1]._attack == templist[highest_idx][1]._attack:
                    if templist[current_idx][1]._cost < templist[highest_idx][1]._cost:
                        highest_idx = current_idx
            else:
                if templist[current_idx][1]._money > templist[highest_idx][1]._money:
                        highest_idx = current_idx
                elif templist[current_idx][1]._money == templist[highest_idx][1]._money:
                    if templist[current_idx][1]._cost < templist[highest_idx][1]._cost:
                        highest_idx = current_idx

        return highest_idx
    
    def check_winner(self):
        winner = False
        if self.player_1._health <= 0:
            winner = True
            print "Computer wins"
        elif self.player_PC._health <= 0:
            winner = True
            print 'Player One Wins'
        elif self.central['active'].size() == 0:
            print "No more cards available"
            if self.player_1._health > self.player_PC._health:
                print "Player One Wins on Health"
            elif self.player_PC._health > self.player_1._health:
                print "Computer Wins"
            else:
                if self.player_1._strength > self.player_PC._strength:
                    print "Player One Wins on Card Strength"
                elif self.player_PC._strength > self.player_1._strength:
                    print "Computer Wins on Card Strength"
                else:
                    print "Draw"
            winner = True
        return winner

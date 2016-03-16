"""
This module implements the game's logic and is used to play to game.
"""
from deckgame.helper import Player, CardsCollection, Card


class Game(object):
    """
    Simulates a game. This is the main class of the game.
    """
    def __init__(self):
        """
        Initialises the game by adding new players and defining the central area.
        """
        self.player_1 = Player('Player 1')
        self.player_pc = Player('Player PC')
        self.central = {'deck': CardsCollection(), 'active': CardsCollection(),
                        'supplement': CardsCollection(), 'active_size': 5}
        self.aggressive = True

    def start_game(self):
        """
        This is the main method of the game. It plays the game until a winner
        is identified.
        """
        self.aggressive = self.get_opponent()
        self.set_up_game()

        winner = False
        while not winner:
            self.player_1_turn()
            self.display_info()
            self.player_pc_turn()
            self.display_info()
            winner = self.check_winner()

    @staticmethod
    def get_opponent():
        """
        Asks the user for the type of the opponent to be used (aggressive or acquisative).
        """
        while True:
            opponent = raw_input("Do you want an aggressive (A) or an acquisative (Q) opponent?")
            if opponent.lower() == 'a':
                print "\nPlaying against aggressive opponent"
                return True
            elif opponent.lower() == 'q':
                print "\nPlaying against acquisative opponent"
                return False
            # check cancel
            else:
                print "\nPlease give a valid option!"

    def set_up_game(self):
        """
        Initialises the game by generating the decks and cards needed.
        It generates the central deck, the pile of supplements, the active
        area cards and the players' decks and hands.
        """
        self.init_central_deck()
        self.init_supplement()

        self.central['deck'].shuffle_collection()
        for _ in range(self.central['active_size']):
            card = self.central['deck'].pop()
            self.central['active'].push(card)

        self.player_1.init_deck()
        self.player_pc.init_deck()

        self.player_1.compute_strength()
        self.player_pc.compute_strength()

        self.player_1.init_hand()
        self.player_pc.init_hand()

    def init_central_deck(self):
        """
        Initialises the central deck by pushing the predefined cards into the
        deck.
        """
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
        """
        Initialises the supplements pile by pushing the predefined cards into the
        pile.
        """
        self.central['supplement'].push(Card('Levy', 1, 2, 2), 10)

    def display_info(self):
        """
        Displays player's information.
        """
        print "\n|----------------------------------------|"
        print "|----------------- INFO -----------------|"
        print "|----------------------------------------|"
        print 'Health:'
        print 'You: %s' % self.player_1.health
        print 'PC: %s' % self.player_pc.health

        print "\nYour Values:"
        self.player_1.print_values()

        print "\nYour Hand:"
        self.player_1.hand.print_collection(indexes=True)

        print "\nYour active area:"
        self.player_1.active.print_collection()

        print "\nAvailable Cards to buy:"
        self.central['active'].print_collection(indexes=True)

        print "\nSupplement:"
        if self.central['supplement'].size() > 0:
            self.central['supplement'].print_card(0)

        print '----------------------------------------'

    def player_1_turn(self):
        """
        This method is responsible for player's (player_1) turn. It asks for
        the action to be taken by printing appropriate messages indicating the
        valid options and calls the corresponding methods.
        """
        while True:
            self.display_info()
            print "\n----------------------------------------"

            if self.player_1.hand.size() > 0 and self.player_1.money > 0 and self.player_1.attack > 0:
                print "Choose Action: (P = Play All, [0-n] = Play Card, B = Buy Card, A = Attack, E = End Turn)"
                valid = ['P', 'B', 'A', 'E'] + map(str, range(self.player_1.hand.size()))
                end_turn = self.player_1_action(valid)
            elif self.player_1.hand.size() > 0 and self.player_1.money > 0:
                print "Choose Action: (P = Play All, [0-n] = Play Card, B = Buy Card, E = End Turn)"
                valid = ['P', 'B', 'E'] + map(str, range(self.player_1.hand.size()))
                end_turn = self.player_1_action(valid)
            elif self.player_1.hand.size() > 0 and self.player_1.attack > 0:
                print "Choose Action: (P = Play All, [0-n] = Play Card, A = Attack, E = End Turn)"
                valid = ['P', 'A', 'E'] + map(str, range(self.player_1.hand.size()))
                end_turn = self.player_1_action(valid)
            elif self.player_1.money > 0 and self.player_1.attack > 0:
                print "Choose Action: (B = Buy Card, A = Attack, E = End turn)"
                valid = ['B', 'A', 'E']
                end_turn = self.player_1_action(valid)
            elif self.player_1.money > 0:
                print "Choose Action: (B = Buy Card, E = End Turn)"
                valid = ['B', 'E']
                end_turn = self.player_1_action(valid)
            elif self.player_1.attack > 0:
                print "Choose Action: (A = Attack, E = End Turn)"
                valid = ['A', 'E']
                end_turn = self.player_1_action(valid)
            elif self.player_1.hand.size() > 0:
                print "Choose Action: (P = Play All, [0-n] = Play Card, E = End Turn)"
                valid = ['P', 'E'] + map(str, range(self.player_1.hand.size()))
                end_turn = self.player_1_action(valid)
            else:
                print "\nNo more possible actions.\nTurn ending."
                self.player_1.end_turn()
                break

            if end_turn:
                break

    def player_1_action(self, valid):
        """
        Gets user's choice, validates it and calls the appropriate method to
        complete the action.
        
        :param valid: a list of valid options for user's input
        :return True: if user decides to end his turn (False otherwise)
        """
        action = raw_input("Enter Action: ")
        if action not in valid:
            print "\nPlease give a valid option!"
        elif action == 'P':
            self.player_1.play_all()
        elif action.isdigit():
            index = int(action)
            self.player_1.play_card(index)
        elif action == 'B':
            self.player_1_buy()
        elif action == 'A':
            self.player_1.attack_opponent(self.player_pc)
        elif action == 'E':
            self.player_1.end_turn()
            return True
        return False

    def player_1_buy(self):
        """
        This method is responsible for player's (player_1) buy action. It asks for
        the card to be bought by printing appropriate messages indicating the
        valid options and calls the corresponding methods.
        """
        while self.player_1.money > 0:
            print "\nAvailable Cards:"
            self.central['active'].print_collection(indexes=True)

            print "\nSupplement:"
            if self.central['supplement'].size() > 0:
                self.central['supplement'].print_card(0)

            print "\nYour Values:"
            self.player_1.print_values()

            buyable_central_cards = any(i.cost <= self.player_1.money for i in self.central['active'].cards)
            if self.central['supplement'].size() > 0:
                buyable_supplement = (self.player_1.money >= self.central['supplement'].cards[0].cost)
            else:
                buyable_supplement = False

            print "\n----------------------------------------"
            if buyable_supplement and buyable_central_cards:
                print "\nChoose a card to buy: ([0-n] = Buy Card, S = Buy Supplement, E = End Buying)"
                valid = ['S', 'E'] + map(str, range(self.central['active'].size()))
                end_buy = self.player_1_buy_option(valid)
            elif buyable_supplement:
                print "\nChoose a card to buy: (S = Buy Supplement, E = End Buying)"
                valid = ['S', 'E']
                end_buy = self.player_1_buy_option(valid)
            elif buyable_central_cards > 0:
                print "\nChoose a card to buy: ([0-n] = Buy Card, E = End Buying)"
                valid = ['E'] + map(str, range(self.central['active'].size()))
                end_buy = self.player_1_buy_option(valid)
            else:
                print "\nNo possible cards to buy"
                break

            print "\nYour Values:"
            self.player_1.print_values()
            if end_buy:
                break

    def player_1_buy_option(self, valid):
        """
        Gets user's choice, validates it and calls the appropriate method to
        complete the action.

        :param valid: a list of valid options for user's input
        :return True: if user decides to end his buy action (False otherwise)
        """
        buy_choice = raw_input("Choose option: ")
        if buy_choice not in valid:
            print "\nPlease give a valid option!"
        elif buy_choice == 'S':
            self.player_1.buy_supplement(self.central['supplement'])
        elif buy_choice.isdigit():
            index = int(buy_choice)
            if self.player_1.money >= self.central['active'].cards[index].cost:
                self.player_1.buy_card(self.central['active'], self.central['deck'], index)
            else:
                print "\nInsufficient money to buy! Please choose another card!"
        elif buy_choice == 'E':
            return True
        return False

    def player_pc_turn(self):
        """
        This method is responsible for computers's (player__pc) turn.
        """
        self.player_pc.play_all()
        print "\nComputer's Turn:"
        print "\nComputer Values:"
        self.player_pc.print_values()

        print "Computer attacking with strength %s..." % self.player_pc.attack
        self.player_pc.attack_opponent(self.player_1)

        print '\nHealth:'
        print "You: %s" % self.player_1.health
        print "PC: %s" % self.player_pc.health
        print "\nComputer Values:"
        self.player_pc.print_values()

        print "Computer buying..."
        self.computer_buy()

        self.player_pc.end_turn()
        print "Computer turn ending"

    def computer_buy(self):
        """
        This method is responsible for computers's (player__pc) buy action.
        It creates a list with the cards that could be bought, based on
        computer's money and calls the appropriate methods in order to find the
        best choice and to buy the card (if any).
        """
        while self.player_pc.money > 0:
            templist = []
            if self.central['supplement'].size() > 0:
                card = self.central['supplement'].cards[0]
                if self.player_pc.money >= card.cost:
                    templist.append(("S", card))
            for i in range(self.central['active'].size()):
                card = self.central['active'].cards[i]
                if self.player_pc.money >= card.cost:
                    templist.append((i, card))
            # check if there are possible cards to buy
            if len(templist) > 0:
                highest_idx = self.computer_best_buy(templist)

                source = templist[highest_idx][0]
                if source in range(self.central['active'].size()):
                    index = int(source)
                    self.player_pc.buy_card(self.central['active'], self.central['deck'], index)
                else:
                    self.player_pc.buy_supplement(self.central['supplement'])
            else:
                break

    def computer_best_buy(self, templist):
        """
        Finds the best card to buy for the computer player, based on a naive
        approach and considering its type (aggressive or acquisative).

        :param templist: a list (of tuples) of possible cards to buy
        :return highest_idx: the index of the best card found in the given list
        """
        highest_idx = 0

        for current_idx in range(len(templist)):
            if self.aggressive:
                if templist[current_idx][1].attack > templist[highest_idx][1].attack:
                    highest_idx = current_idx
                elif templist[current_idx][1].attack == templist[highest_idx][1].attack:
                    if templist[current_idx][1].cost < templist[highest_idx][1].cost:
                        highest_idx = current_idx
            else:
                if templist[current_idx][1].money > templist[highest_idx][1].money:
                    highest_idx = current_idx
                elif templist[current_idx][1].money == templist[highest_idx][1].money:
                    if templist[current_idx][1].cost < templist[highest_idx][1].cost:
                        highest_idx = current_idx

        return highest_idx

    def check_winner(self):
        """
        Check whether there is a winner, based on players' health, strength
        and on central deck's size.

        :return winner: True if a winner has been found
        """
        winner = False
        if self.player_1.health <= 0:
            winner = True
            print "Computer wins"
        elif self.player_pc.health <= 0:
            winner = True
            print "Player One Wins"
        elif self.central['active'].size() == 0:
            print "No more cards available"
            if self.player_1.health > self.player_pc.health:
                print "Player One Wins on Health"
            elif self.player_pc.health > self.player_1.health:
                print "Computer Wins"
            else:
                if self.player_1.strength > self.player_pc.strength:
                    print "Player One Wins on Card Strength"
                elif self.player_pc.strength > self.player_1.strength:
                    print "Computer Wins on Card Strength"
                else:
                    print "Draw"
            winner = True
        return winner

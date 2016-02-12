# on separate lines
import itertools, random

class Card(object):
    def __init__(self, name, values=(0, 0), cost=1, clan=None):
        self.name = name
        self.cost = cost
        self.values = values
        # dead code
        self.clan = clan
    def __str__(self):
                return 'Name %s costing %s with attack %s and money %s' % (self.name, self.cost, self.values[0], self.values[1])
    def get_attack(self):
        return self.values[0]
    def get_money(self):
            return self.values[1]


if __name__ == '__main__':
    # Player class
    pO = {'name': 'player one', 'health': 30, 'deck': None, 'hand': None, 'active': None, 'handsize': 5,
                 'discard': None}
    pC = {'name': 'player computer', 'health': 30, 'deck': None, 'hand': None, 'active': None, 'handsize': 5,
               'discard': None}
    central = {'name': 'central', 'active': None, 'activeSize': 5, 'supplement': None, 'deck': None}
    # long line
    sdc = [4 * [Card('Archer', (3, 0), 2)], 4 * [Card('Baker', (0, 3), 2)], 3 * [Card('Swordsman', (4, 0), 3)], 2 * [Card('Knight', (6, 0), 5)],3 * [Card('Tailor', (0, 4), 3)],3 * [Card('Crossbowman', (4, 0), 3)],3 * [Card('Merchant', (0, 5), 4)],4 * [Card('Thug', (2, 0), 1)],4 * [Card('Thief', (1, 1), 1)],2 * [Card('Catapault', (7, 0), 6)], 2 * [Card('Caravan', (1, 5), 5)],2 * [Card('Assassin', (5, 0), 4)]]

    playeronedeck = [8 * [Card('Serf', (0, 1), 0)],
                     2 * [Card('Squire', (1, 0), 0)]
                     ]
    pod = list(itertools.chain.from_iterable(playeronedeck))
    pO['deck'] = pod
    pO['hand'] = []
    pO['discard'] = []
    pO['active'] = []
    # same with playeronedeck
    playertwodeck = [
            8 * [Card('Serf', (0, 1), 0)],
        2 * [Card('Squire', (1, 0), 0)]
    ]
    ptd = list(itertools.chain.from_iterable(playertwodeck))
    pC['deck'] = ptd
    pC['hand'] = []
    pC['discard'] = []
    pC['active'] = []

    supplement = 10 * [Card('Levy', (1, 2), 2)]
    deck = list(itertools.chain.from_iterable(sdc))

    random.shuffle(deck)
    central['deck'] = deck
    central['supplement'] = supplement
    central['active'] = []

    # max built-in function
    max = central['activeSize']
    count = 0
    while count < max:
        card = central['deck'].pop()
        central['active'].append(card)
        count = count + 1

    # len(p0['hand'])
    for x in range(0, pO['handsize']):
        # no need for parentheses
        if (len(pO['deck']) == 0):
            random.shuffle(pO['discard'])
            pO['deck'] = pO['discard']
            pO['discard'] = []
        card = pO['deck'].pop()
        pO['hand'].append(card)

    # pC['handside'] or len(pC['hand'])
    for x in range(0, pO['handsize']):
        if len(pC['deck']) == 0:
            # random.shuffle(pC['discard'])
            random.shuffle(pO['discard'])
            pC['deck'] = pC['discard']
            pC['discard'] = []
        card = pC['deck'].pop()
        pC['hand'].append(card)

    print "Available Cards"
    for card in central['active']:
        print card

    print "Supplement"
    if len(central['supplement']) > 0:
        # central['supplement']
        print central['supplement'][0]


    # (Y) for yes, (N) for No, or even handle Yes, YES etc.
    pG = raw_input('Do you want to play a game?:')
    
    cG = (pG=='Y')
    # check if N to exit
    oT = raw_input("Do you want an aggressive (A) opponent or an acquisative (Q) opponent")
    aggressive = (oT=='A')
    while cG:
        money = 0
        attack = 0
        while True:

            print "\nPlayer Health %s" % pO['health']
            print "Computer Health %s" % pC['health']

            print "\nYour Hand"
            # use enumerate or for i in range
            index = 0
            for card in pO['hand']:
                # fix indentation
                    print "[%s] %s" % (index, card)
                    index = index + 1
            print "\nYour Values"
            print "Money %s, Attack %s" % (money, attack)
            print "\nChoose Action: (P = play all, [0-n] = play that card, B = Buy Card, A = Attack, E = end turn)"
            # handle invalid input
            act = raw_input("Enter Action: ")
            print act
            # function play_all(p0)
            # or http://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement
            if act == 'P':
                # no need for this statement (for iterates up to len()), no need for parentheses
                if(len(pO['hand'])>0):
                    # list modification under iteration, replace with while p0['hand'] (?)
                    # better to have cards in the right order 
                    # for i in range(len(a) - 1, -1, -1):
                    #     card = a.pop(i)
                    for x in range(0, len(pO['hand'])):
                        # no need to store to variable
                        card = pO['hand'].pop()
                        pO['active'].append(card)
                        money = money + card.get_money()
                        attack = attack + card.get_attack()

                # method print_card(list, index=False)
                print "\nYour Hand"
                # use enumerate or for i in range
                index = 0
                for card in pO['hand']:
                    print "[%s] %s" % (index, card)
                    index = index + 1

                print "\nYour Active Cards"
                for card in pO['active']:
                    print card
                print "\nYour Values"
                print "Money %s, Attack %s" % (money, attack)
            if act.isdigit():
                # handle invalid input (>len()) printing msg
                # no need for parentheses
                if( int(act) < len(pO['hand'])):
                    # could be a method to avoid duplication               
                    pO['active'].append(pO['hand'].pop(int(act)))
                    for card in pO['active']:
                        money = money + card.get_money()
                        attack = attack + card.get_attack()
                print "\nYour Hand"
                # use enumerate or for i in range
                index = 0
                for card in pO['hand']:
                    print "[%s] %s" % (index, card)
                    index = index + 1

                print "\nYour Active Cards"
                for card in pO['active']:
                    print card
                print "\nYour Values"
                print "Money %s, Attack %s" % (money, attack)
            # no need for parenthesis 
            if (act == 'B'):
                # if money > 0, while notending... 
                notending = True
                while money > 0:
                    print "Available Cards"
                    # use enumerate or for i in range
                    ind = 0
                    for card in central['active']:
                        print "[%s] %s" % (ind,card)
                        ind = ind + 1
                    print "Choose a card to buy [0-n], S for supplement, E to end buying"
                    bv = raw_input("Choose option: ")
                    if bv == 'S':
                        if len(central['supplement']) > 0:
                            if money >= central['supplement'][0].cost:
                                # bug found, checks index 0 but pop removes last item, use pop(0)
                                money = money - central['supplement'][0].cost
                                pO['discard'].append(central['supplement'].pop())
                                print "Supplement Bought"
                            else:
                                print "insufficient money to buy"
                        else:
                            # handle this
                            print "no supplements left"
                    elif bv == 'E':
                        notending = False
                        # unnecessary semicolon
                        break;
                    elif bv.isdigit():
                        if int(bv) < len(central['active']):
                            # wrong indentation
                             if money >= central['active'][int(bv)].cost:
                                money = money - central['active'][int(bv)].cost
                                pO['discard'].append(central['active'].pop(int(bv)))
                                # unnecessary parentheses
                                if( len(central['deck']) > 0):
                                    # no need to store to variable (consider cohesion)
                                    card = central['deck'].pop()
                                    central['active'].append(card)
                                else:
                                    # no need for activeSize variable
                                    central['activeSize'] = central['activeSize'] - 1
                                print "Card bought"
                             else:
                                print "insufficient money to buy"
                        else:
                            # handle with while
                             print "enter a valid index number"
                    else:
                        # handle with while
                        print "Enter a valid option"


            if act == 'A':
                # does it count only active area?
                pC['health'] = pC['health'] - attack
                attack = 0
            if act == 'E':
                # no need to check
                if (len(pO['hand']) >0 ):
                    for x in range(0, len(pO['hand'])):
                        pO['discard'].append(pO['hand'].pop())

                # no need to check
                if (len(pO['active']) >0 ):
                    for x in range(0, len(pO['active'])):
                        pO['discard'].append(pO['active'].pop())
                # replace pO['handsize'] with len(p0['hand'])
                # why shuffle in every iteration? (inefficient)
                for x in range(0, pO['handsize']):
                    if len(pO['deck']) == 0:
                        # check if discard empty?
                        random.shuffle(pO['discard'])
                        pO['deck'] = pO['discard']
                        pO['discard'] = []
                    card = pO['deck'].pop()
                    pO['hand'].append(card)
                break

        print "Available Cards"
        for card in central['active']:
            print card

        print "Supplement"
        if len(central['supplement']) > 0:
            print central['supplement'][0]

        print "\nPlayer Health %s" % pO['health']
        print "Computer Health %s" % pC['health']

        money = 0
        attack = 0
        # eliminate duplication
        for x in range(0, len(pC['hand'])):
                        card = pC['hand'].pop()
                        pC['active'].append(card)
                        money = money + card.get_money()
                        attack = attack + card.get_attack()

        print " Computer player values attack %s, money %s" % (attack, money)
        print " Computer attacking with strength %s" % attack
        pO['health'] = pO['health'] - attack
        attack = 0
        print "\nPlayer Health %s" % pO['health']
        print "Computer Health %s" % pC['health']

        print " Computer player values attack %s, money %s" % (attack, money)
        print "Computer buying"
        if money > 0:
            cb = True
            templist = []
            # no need to print cb
            print "Starting Money %s and cb %s " % (money, cb)
            while cb:
                templist = []
                if len(central['supplement']) > 0:
                    if central['supplement'][0].cost <= money:
                        # append to pC['discard'], pop from central['active']
                        templist.append(("S", central['supplement'][0]))
                # replace activeSize with len()
                for intindex in range (0, central['activeSize']):
                    if central['active'][intindex].cost <= money:             
                        templist.append((intindex, central['active'][intindex]))
                if len(templist) >0:
                    highestIndex = 0
                    # start from 1
                    # find index with highest cost at first, then check aggressive etc.
                    for intindex in range(0,len(templist)):
                        if templist[intindex][1].cost > templist[highestIndex][1].cost:
                            highestIndex = intindex
                        if templist[intindex][1].cost == templist[highestIndex][1].cost:
                            if aggressive:
                                if templist[intindex][1].get_attack() >templist[highestIndex][1].get_attack():
                                    highestIndex = intindex
                            else:
							    # get_money instead of get_attack
                                if templist[intindex][1].get_attack() >templist[highestIndex][1].get_money():
                                    highestIndex = intindex
                    source = templist[highestIndex][0]
                    # replace 5 with activeSize
                    if source in range(0,5):
                        if money >= central['active'][int(source)].cost:
                            money = money - central['active'][int(source)].cost
                            card = central['active'].pop(int(source))
                            print "Card bought %s" % card
                            pC['discard'].append(card)
                            # unnecessary parentheses
                            if( len(central['deck']) > 0):
                                # no need to store in variable
                                card = central['deck'].pop()
                                central['active'].append(card)
                            else:
                                # no need for this if we have len(central['active'])
                                central['activeSize'] = central['activeSize'] - 1
                        else:
                            # this should not happen, check
                            print "Error Occurred"
                    else:
                        if money >= central['supplement'][0].cost:
                            money = money - central['supplement'][0].cost
                            # pop(0)
                            card = central['supplement'].pop()
                            pC['discard'].append(card)
                            print "Supplement Bought %s" % card
                        else:
                            # handle this
                            print "Error Occurred"
                else:
                    cb = False
                if money == 0:
                    cb = False
        else:
            print "No Money to buy anything"

        # no need to check
        if (len(pC['hand']) >0 ):
            for x in range(0, len(pC['hand'])):
                pC['discard'].append(pC['hand'].pop())
        if (len(pC['active']) >0 ):
            for x in range(0, len(pC['active'])):
                pC['discard'].append(pC['active'].pop())
        # put to function to eliminate duplication
        for x in range(0, pC['handsize']):
                    if len(pC['deck']) == 0:
                        random.shuffle(pC['discard'])
                        pC['deck'] = pC['discard']
                        pC['discard'] = []
                    card = pC['deck'].pop()
                    pC['hand'].append(card)
        print "Computer turn ending"


        print "Available Cards"
        for card in central['active']:
            print card

        print "Supplement"
        if len(central['supplement']) > 0:
            print central['supplement'][0]

        print "\nPlayer Health %s" % pO['health']
        print "Computer Health %s" % pC['health']

        # insert to function print_winner
        if pO['health'] <= 0:
            cG = False
            print "Computer wins"
        elif pC['health'] <= 0:
            cG = False
            print 'Player One Wins'
        # len(central)   
        elif central['activeSize'] == 0:
            print "No more cards available"
            if pO['health'] > pC['health']:
                print "Player One Wins on Health"
            elif pC['health'] > pO['health']:
                print "Computer Wins"
            else:
                # pHt = p0['strength'] compute it
                # pCT = pC['strength'] compute it
                pHT = 0
                pCT = 0
                if pHT > pCT:
                    print "Player One Wins on Card Strength"
                elif pCT > pHT:
                    print "Computer Wins on Card Strength"
                else:
                    print "Draw"
            cG = False
        if not cG:
            #duplicate, insert to function initialise()
            pG = raw_input("\nDo you want to play another game?:")
            cG = (pG=='Y')
            if cG:
                oT = raw_input("Do you want an aggressive (A) opponent or an acquisative (Q) opponent")
                aggressive = (oT=='A')
                pO = {'name': 'player one', 'health': 30, 'deck': None, 'hand': None, 'active': None,
                             'handsize': 5,
                             'discard': None}
                pC = {'name': 'player computer', 'health': 30, 'deck': None, 'hand': None, 'active': None, 'handsize': 5,
                            'discard': None}
                central = {'name': 'central', 'active': None, 'activeSize': 5, 'supplement': None, 'deck': None}
                
                sdc = [
                                4 * [Card('Archer', (3, 0), 2)],
                                4 * [Card('Baker', (0, 3), 2)],
                                3 * [Card('Swordsman', (4, 0), 3)],
                                2 * [Card('Knight', (6, 0), 5)],
                                3 * [Card('Tailor', (0, 4), 3)],
                                3 * [Card('Crossbowman', (4, 0), 3)],
                                3 * [Card('Merchant', (0, 5), 4)],
                                4 * [Card('Thug', (2, 0), 1)],
                                4 * [Card('Thief', (1, 1), 1)],
                                2 * [Card('Catapault', (7, 0), 6)],
                                2 * [Card('Caravan', (1, 5), 5)],
                                2 * [Card('Assassin', (5, 0), 4)]
                            ]
                playeronedeck = [8 * [Card('Serf', (0, 1), 0)],
                                 2 * [Card('Squire', (1, 0), 0)]
                            ]
                pod = list(itertools.chain.from_iterable(playeronedeck))
                pO['deck'] = pod
                pO['hand'] = []
                pO['discard'] = []
                pO['active'] = []
                playertwodeck = [
                            8 * [Card('Serf', (0, 1), 0)],
                            2 * [Card('Squire', (1, 0), 0)]
                ]
                ptd = list(itertools.chain.from_iterable(playertwodeck))
                pC['deck'] = ptd
                pC['hand'] = []
                pC['discard'] = []
                pC['active'] = []

                supplement = 10 * [Card('Levy', (1, 2), 2)]
                deck = list(itertools.chain.from_iterable(sdc))
                random.shuffle(deck)
                central['deck'] = deck
                central['supplement'] = supplement
                central['active'] = []

                for x in range(0, central['activeSize']):
                    card = central['deck'].pop()
                    central['active'].append(card)

                for x in range(0, pO['handsize']):
                    if len(pO['deck']) == 0:
                        random.shuffle(pO['discard'])
                        pO['deck'] = pO['discard']
                        pO['discard'] = []
                    card = pO['deck'].pop()
                    pO['hand'].append(card)

                for x in range(0, pO['handsize']):
                    if len(pC['deck']) == 0:
                        random.shuffle(pO['discard'])
                        pC['deck'] = pC['discard']
                        pC['discard'] = []
                    card = pC['deck'].pop()
                    pC['hand'].append(card)


                print "Available Cards"
                # replace with for (for c in central['active']: print c)
                max = central['activeSize']
                count = 0
                while count < max:
                    print central['active'][count]
                    count = count + 1

                print "Supplement"
                if len(central['supplement']) > 0:
                    print central['supplement'][0]
    exit()


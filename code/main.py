import sys

import deckgame as dg

def main():
    '''f = open('game.log', 'w')
    original = sys.stdout
    sys.stdout = dg.helper.Tee(sys.stdout, f)'''
    #sys.stdout = log_file
    while True:
        pG = raw_input('Do you want to start a new game?')
        if pG.lower() =='y':
            new_game = True
        elif pG.lower() =='n':
            new_game = False
        else:
            print 'Please give a valid option!'
            continue
        if new_game:
            cg = dg.game.Game()
            cg.start_game()
        else:
            break

    '''sys.stdout = original
    f.close()'''

    exit()

if __name__ == '__main__':
    main()
    

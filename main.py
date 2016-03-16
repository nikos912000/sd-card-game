#import sys
import deckgame as dg


def main():
    '''f = open('game.log', 'w')
    original = sys.stdout
    sys.stdout = dg.helper.Tee(sys.stdout, f)'''
    #sys.stdout = log_file
    while True:
        new_game = raw_input("Do you want to start a new game?")
        if new_game.lower() == 'y':
            start_game = True
        elif new_game.lower() == 'n':
            start_game = False
        else:
            print "Please give a valid option!"
            continue
        if start_game:
            deck_game = dg.game.Game()
            deck_game.start_game()
        else:
            break

    '''sys.stdout = original
    f.close()'''

    exit()

if __name__ == '__main__':
    main()

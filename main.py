"""
Main script that starts a new game.
"""
#import sys
import deckgame as dg


def main():
    """
    Starts a new game.
    """
    while True:
        new_game = raw_input("Do you want to start a new game (Y for Yes, N for No)?")
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
    exit()

if __name__ == '__main__':
    main()

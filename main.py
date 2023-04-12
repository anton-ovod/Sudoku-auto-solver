import pygame
from GUI.Window import SudokuGUI

# initialize the pygame runtime
pygame.init()
# set caption for game window
pygame.display.set_caption('Sudoku Puzzles Solver')
# load icon for game
icon = pygame.image.load('images/game_logo.png')
# set icon for the game
pygame.display.set_icon(icon)


def main_game():
    """main method to be called"""
    # infinite loop
    while True:
        sg = SudokuGUI()
        started = 0
        # run while the main_menu doesn't generate a valid option
        while not started:
            started = sg.main_menu()
        # if play game option is selected
        if started:
            while sg.play_game():
                pass
        pygame.display.update()


if __name__ == '__main__':
    main_game()
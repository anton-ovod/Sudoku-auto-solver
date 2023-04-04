# import environment variable from os
import os
# import GUI for error boxes
import tkinter.messagebox
# import GUI for file and error notifications
from tkinter import Tk
# import supress to ignore any exceptions
from contextlib import suppress
# import choice to choose between GUI screen
from random import choice
# import sleep to add delay between GUI screen
from time import sleep
# import respective object type for hint specification
from typing import List, Tuple

os.environ['SDL_VIDEO_CENTERED'] = '1'

# import numpy module for operations on image matrices
import numpy as np
# import pygame module
import pygame

# import Button class for mouse action buttons in the GUI
from GUI.Button import Button
# import Sudoku class to solve the puzzle using Algorithm X
from sudoku import Sudoku

# initialize the root window
root = Tk()
# hide root window
root.withdraw()

# pixel size of cells in the pygame
BLOCK_SIZE = 40
# width of game screen
SCREEN_WIDTH = 650
# height of game screen
SCREEN_HEIGHT = 650
# global constant for indexing coordinates
X = 0
Y = 1


class SudokuGUI:
    """Template Class for the GUI in the game"""

    # type hints for the class variables
    BOX_ROWS: int
    BOX_COLS: int
    NUM_ROWS: int
    NUM_COLUMNS: int
    PLAY_WIDTH: int
    PLAY_HEIGHT: int
    TOP_LEFT: Tuple[int, int]
    matrix: np.ndarray
    solution_list: List[int, int]
    solution: np.ndarray
    window: pygame.Surface
    selected_box: Tuple[int, int]
    locked_pos: List[Tuple[int, int]]
    home_icon: pygame.Surface
    button_home: Button
    button_solve: Button
    button_play_game: Button

    def __init__(self, matrix: np.ndarray, box_rows: int = 3, box_cols: int = 3):
        """default initialization"""

        # ========================== GUI Parameters ============================
        # set number of rows in the sub grid
        self.BOX_ROWS = box_rows
        # set number of columns in the sub grid
        self.BOX_COLS = box_cols
        # number of rows in the game
        self.NUM_ROWS = self.BOX_ROWS * self.BOX_COLS
        # number of columns in the game
        self.NUM_COLUMNS = self.BOX_ROWS * self.BOX_COLS
        # width of the play area
        self.PLAY_WIDTH = BLOCK_SIZE * self.NUM_COLUMNS
        # height of the play area
        self.PLAY_HEIGHT = BLOCK_SIZE * self.NUM_ROWS
        # top left coordinates of where the game will be placed
        self.TOP_LEFT = (int((SCREEN_WIDTH - self.PLAY_WIDTH) / 2),
                         int((SCREEN_HEIGHT - self.PLAY_HEIGHT) / 2 - 80))

        # ========================== Game Parameters ===========================
        # puzzle matrix for the game
        self.matrix = matrix
        # copy of the initial matrix
        self.init_matrix = self.matrix.copy()
        try:
            # find the solutions for the given matrix
            self.solution_list = Sudoku(matrix.copy(), box_row=self.BOX_ROWS, box_col=self.BOX_COLS).get_solution()
            # take the first solution
            self.solution = self.solution_list[0]
        except Exception:
            # in case no solution show error
            tkinter.messagebox.showerror(title="Error", message="Solutions does not exist, Try again.")

        # create screen for the game window
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # default box selected
        self.selected_box = (0, 0)
        # list of coordinates for the clues in the puzzle
        self.locked_pos = self.get_locked_pos()
        # icon for the home button
        self.home_icon = pygame.image.load("images/home_icon.png")
        # home button object
        self.button_home = Button(60, 60, 70, 70, (200, 200, 200), '  ')
        # solve the current puzzle button
        self.button_solve = Button(325, 590, 250, 60, (200, 200, 200), "Solve")
        # play game button
        self.button_play_game = Button(325, 300, 400, 80, (200, 200, 200), "Play Game")

    def get_locked_pos(self):
        """Get list of coordinates of the clues in the given puzzle"""

        # initialize emtpy list
        locked_pos = []
        # iterate through rows
        for i in range(self.NUM_ROWS):
            # iterate through columns
            for j in range(self.NUM_COLUMNS):
                # if clue i.e. non zero
                if self.matrix[i, j] != 0:
                    # than add to locked_pos
                    locked_pos.append((i, j))
        # return the list
        return locked_pos

    def draw_window(self, solved: bool = False):
        """Draw the window for the game"""

        # background color for the game
        self.window.fill((255, 255, 255))

        # heading font
        font = pygame.font.SysFont('comicsans', 48)
        # heading label
        label = font.render("SUDOKU", 1, (0, 0, 0))
        # display the label
        self.window.blit(label,
                         (self.TOP_LEFT[X] + self.PLAY_WIDTH / 2 - (label.get_width() / 40 - (label.get_height() / 2))))

        # draw reference grid black lines
        for i in range(self.NUM_ROWS):
            # horizontal lines
            pygame.draw.line(self.window, (0, 0, 0),
                             (self.TOP_LEFT[X], self.TOP_LEFT[Y] + i * BLOCK_SIZE),
                             (self.TOP_LEFT[X] + self.PLAY_WIDTH,
                              self.TOP_LEFT[Y] + i * BLOCK_SIZE),
                             4 if i % self.BOX_ROWS == 0 else 1)
        for i in range(self.NUM_COLUMNS):
            # vertical lines
            pygame.draw.line(self.window, (0, 0, 0),
                             (self.TOP_LEFT[X] + i * BLOCK_SIZE,
                              self.TOP_LEFT[Y]),
                             (self.TOP_LEFT[X] + i * BLOCK_SIZE,
                              self.TOP_LEFT[Y] + self.PLAY_HEIGHT),
                             4 if i % self.BOX_COLS == 0 else 1)
        # last horizontal line
        pygame.draw.line(self.window, (0, 0, 0),
                         (self.TOP_LEFT[X],
                          self.TOP_LEFT[Y] + self.NUM_ROWS * BLOCK_SIZE),
                         (self.TOP_LEFT[X] + self.PLAY_WIDTH,
                          self.TOP_LEFT[Y] + self.NUM_ROWS * BLOCK_SIZE), 4)

        # last vertical line
        pygame.draw.line(self.window, (0, 0, 0),
                         (self.TOP_LEFT[X] + self.NUM_COLUMNS * BLOCK_SIZE,
                          self.TOP_LEFT[Y]),
                         (self.TOP_LEFT[X] + self.NUM_COLUMNS * BLOCK_SIZE,
                          self.TOP_LEFT[Y] + self.PLAY_HEIGHT), 4)

        # font for the numbers, with different size
        font = pygame.font.SysFont('comicsans', 32)

        # iterate through rows
        for i in range(self.NUM_ROWS):
            # iterate through columns
            for j in range(self.NUM_COLUMNS):
                # cell is empty
                if self.matrix[i, j] == 0:
                    continue

                if (i, j) in self.locked_pos:
                    # the color is black
                    num_color = (0, 0, 0)
                # if it has been solved
                elif solved:
                    # the color is green
                    num_color = (128, 193, 42)
                # if it is valid value
                elif Sudoku.element_possible(self.matrix, self.BOX_ROWS, self.BOX_COLS, i, j):
                    # the color is blue
                    num_color = (89, 154, 252)
                # if it is not valid
                else:
                    # color is red
                    num_color = (255, 0, 0)

                # generate label for the value
                label = font.render(str(self.matrix[i, j]), 1, num_color)
                # display label on screen
                self.window.blit(label,
                                 (self.TOP_LEFT[X] + j * BLOCK_SIZE - label.get_width() / 2 + BLOCK_SIZE / 2,
                                  self.TOP_LEFT[Y] + i * BLOCK_SIZE - label.get_height() / 2 + BLOCK_SIZE / 2))

                # highlight border of the selected box
                pygame.draw.rect(self.window, (100, 178, 255),
                                 (self.TOP_LEFT[X] + self.selected_box[0] * BLOCK_SIZE,
                                  self.TOP_LEFT[Y] + self.selected_box[1] * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 4)

                # display the home button
                self.button_home.draw(self.window)
                # display the icon on the home button
                self.window.blit(self.home_icon,
                                 (self.button_home.x - self.home_icon.get_width() / 2,
                                  self.button_home.y - self.home_icon.get_height() / 2))

                # display the solve button
                self.button_solve.draw(self.window)
                # update the display to reflect the above changes
                pygame.display.update()

# import environment variable from os
import os

# import choice to choose between the empty cells
from random import choice

# import sleep to add delay between GUI screen
from time import sleep

# import GUI for file and error notifications
from tkinter import Tk

# import respective object type for type hint specification
from typing import List, Tuple

from math import sqrt

# set the environment variable to open the GUI in the center of the screen
os.environ["SDL_VIDEO_CENTERED"] = "1"

# import numpy module for operations on image matrices
import numpy as np

# import pygame module
import pygame

# import Button class for mouse action buttons in the GUI
from GUI.Button import Button

# import Sudoku class to solve the puzzle using Algorithm X
from sudoku import Sudoku

X = 0
Y = 1


class SudokuGUI:
    """Template Class for the GUI in the game"""

    def __init__(self):
        """default initialization"""
        # size of matrix
        self.SIZE = 9
        # number of rows and columns in the box
        self.BOX_ROWS = 3
        self.BOX_COLS = 3
        # size of the block
        self.BLOCK_SIZE = 30
        # width of the play area
        self.PLAY_WIDTH = 9 * self.BLOCK_SIZE
        # height of the play area
        self.PLAY_HEIGHT = 9 * self.BLOCK_SIZE
        # width of the game window
        self.WINDOW_WIDTH = 650
        # height of the game window
        self.WINDOW_HEIGHT = 650
        # top left coordinates of where the game will be placed
        self.TOP_LEFT = (0, 0)

        # ========================== Game Parameters ===========================
        # puzzle matrix for the game
        self.matrix: np.ndarray = None
        # create screen for the gma window
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        # default box selected
        self.selected_box = (0, 0)
        # solution matrix for the game
        self.solution: np.ndarray = None
        # matrix for the clues in the game
        self.locked_pos: List = []

        # ========================== GUI Buttons ===============================
        # icon for the home button
        self.home_icon = pygame.image.load("images/home_icon.png")
        # home button object
        self.button_home = Button(60, 60, 70, 70, (200, 200, 200), "  ")
        # solve the current puzzle button
        self.button_solve = None

        # play game button
        self.button_play_game = Button(325, 580, 400, 80, (200, 200, 200), "Play Game")
        # first available size of grid button
        self.button_4x4 = Button(150, 300, 200, 80, (200, 200, 200), "4x4")
        # second available size of grid button
        self.button_9x9 = Button(500, 300, 200, 80, (200, 200, 200), "9x9")
        # third available size of grid button
        self.button_16x16 = Button(150, 425, 200, 80, (200, 200, 200), "16x16")
        # fourth available size of grid button
        self.button_25x25 = Button(500, 425, 200, 80, (200, 200, 200), "25x25")

    def get_locked_pos(self):
        """Get list of coordinates of the clues in the given puzzle"""

        # initialize empty list
        locked_pos = []
        # iterate through rows
        for i in range(self.SIZE):
            # iterate through columns
            for j in range(self.SIZE):
                # if clue i.e. non zero
                if self.matrix[i, j] != 0:
                    # then add to locked_pos
                    locked_pos.append((i, j))
        # return the list
        return locked_pos

    def handle_click(self, event):
        """This method helps handle left mouse clicks"""

        # check if solve button is clicked
        if self.button_solve.clicked(event):
            self.solution = Sudoku(
                self.matrix.copy(), box_row=self.BOX_ROWS, box_col=self.BOX_COLS
            ).get_solution()
            print(self.solution)
            while 0 in self.matrix:
                # find positions of empty cells
                rows, cols = np.where(self.matrix == 0)
                # choose a random coordinate of an empty cell
                coords = choice(list(zip(rows, cols)))
                row, col = coords
                self.selected_box = col, row
                self.matrix[coords] = self.solution[coords]
                # delay to better visualize
                sleep(0.1)
                # draw the entries with green color
                self.draw_window(solved=True)

        # check if home button is clicked
        if self.button_home.clicked(event):
            # go back to main menu
            return False

        if event.type == pygame.QUIT:
            # if quit button is clicked, exit the game
            pygame.quit()
            exit()

        # if LEFT mouse button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # get the current coordinates of the mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # convert to integer
            mouse_x, mouse_y = int(mouse_x), int(mouse_y)
            # if mouse coordinates during the click are in the range of the game area
            if mouse_x in range(
                    self.TOP_LEFT[X], self.TOP_LEFT[X] + self.SIZE * self.BLOCK_SIZE
            ) and mouse_y in range(
                self.TOP_LEFT[Y], self.TOP_LEFT[Y] + self.SIZE * self.BLOCK_SIZE
            ):
                # select the box in which the mouse is clicked
                self.selected_box = (
                    (mouse_x - self.TOP_LEFT[X]) // self.BLOCK_SIZE,
                    (mouse_y - self.TOP_LEFT[Y]) // self.BLOCK_SIZE,
                )

        # default return is True
        return True

    def play_game(self):
        """This method handles the input part of the Game"""
        if np.array_equal(self.matrix, self.solution):
            self.draw_window(solved=True)
        else:
            # display the game GUI
            self.draw_window()
        for event in pygame.event.get():

            # check for any click, return True if home is pressed
            if not self.handle_click(event):
                # return to the main menu
                return False

            # if a key is pressed
            if event.type == pygame.KEYDOWN:
                # get coordinates of selected box
                box_i, box_j = self.selected_box

                # if up arrow key
                if event.key == pygame.K_UP:
                    # shift the selected box up
                    box_j -= 1
                # if down arrow key
                if event.key == pygame.K_DOWN:
                    # shift the selected box down
                    box_j += 1
                # if right arrow key
                if event.key == pygame.K_RIGHT:
                    # shift the selected box right
                    box_i += 1
                # if left arrow key
                if event.key == pygame.K_LEFT:
                    # shift the selected box left
                    box_i -= 1
                # update the selected box
                self.selected_box = (box_i % self.SIZE, box_j % self.SIZE)

                if (
                        event.key
                        in (
                        pygame.K_0,
                        pygame.K_1,
                        pygame.K_2,
                        pygame.K_3,
                        pygame.K_4,
                        pygame.K_5,
                        pygame.K_6,
                        pygame.K_7,
                        pygame.K_8,
                        pygame.K_9,
                )
                        and (box_j, box_i) not in self.locked_pos
                ):
                    potential = int(
                        str(self.matrix[box_j, box_i]) + str(event.key - 48)
                    )
                    if len(str(potential)) < 2 and potential <= self.SIZE:
                        self.matrix[box_j, box_i] = potential
                    elif len(str(potential)) == 2 and potential <= self.SIZE:
                        self.matrix[box_j, box_i] = int(
                            str(self.matrix[box_j, box_i])[0] + str(event.key - 48)
                        )
                if (
                        event.key == pygame.K_BACKSPACE
                        and (box_j, box_i) not in self.locked_pos
                ):
                    self.matrix[box_j, box_i] = (
                        int(str(self.matrix[box_j, box_i])[:-1])
                        if len(str(self.matrix[box_j, box_i])) > 1
                        else 0
                    )
                if (
                        event.key == pygame.K_RETURN
                        and self.matrix[box_j, box_i]
                        and (box_j, box_i) not in self.locked_pos
                        and Sudoku.element_possible(self.matrix, self.SIZE, box_j, box_i)
                ):
                    self.locked_pos.append((box_j, box_i))
                    print(self.locked_pos)


        pygame.display.update()
        return True

    def main_menu(self):
        """Shows the menu for the program"""

        # fill the background
        self.window.fill((255, 255, 255))
        # font for the heading
        font = pygame.font.SysFont("comicsans", 60)
        # label for the heading
        label = font.render("Sudoku Solver", 1, (0, 0, 0))
        # display the heading
        self.window.blit(
            label, ((650 - label.get_width()) / 2, 100 - label.get_height() / 2)
        )
        # iterate through events
        for event in pygame.event.get():
            # if play game button is pressed
            if self.button_play_game.clicked(event):
                self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
                self.matrix = np.zeros((self.SIZE, self.SIZE), dtype=int)
                self.locked_pos = self.get_locked_pos()
                return 1
            if self.button_4x4.clicked(event):
                self.button_4x4.pressed = True
                self.button_9x9.pressed = False
                self.button_16x16.pressed = False
                self.button_25x25.pressed = False
                self.SIZE = 4
                self.BLOCK_SIZE = 50
                self.WINDOW_HEIGHT = 500
                self.WINDOW_WIDTH = 500
                self.BOX_ROWS = self.BOX_COLS = sqrt(self.SIZE)
                self.PLAY_WIDTH = self.BLOCK_SIZE * self.SIZE
                self.PLAY_HEIGHT = self.BLOCK_SIZE * self.SIZE
                self.TOP_LEFT = (
                    self.WINDOW_WIDTH // 2 - self.PLAY_WIDTH // 2,
                    self.WINDOW_HEIGHT // 2 - self.PLAY_HEIGHT // 2,
                )
            if self.button_9x9.clicked(event):
                self.button_4x4.pressed = False
                self.button_9x9.pressed = True
                self.button_16x16.pressed = False
                self.button_25x25.pressed = False
                self.SIZE = 9
                self.BLOCK_SIZE = 40
                self.WINDOW_HEIGHT = 600
                self.WINDOW_WIDTH = 600
                self.BOX_ROWS = self.BOX_COLS = sqrt(self.SIZE)
                self.PLAY_WIDTH = self.BLOCK_SIZE * self.SIZE
                self.PLAY_HEIGHT = self.BLOCK_SIZE * self.SIZE
                self.TOP_LEFT = (
                    self.WINDOW_WIDTH // 2 - self.PLAY_WIDTH // 2,
                    self.WINDOW_HEIGHT // 2 - self.PLAY_HEIGHT // 2,
                )
            if self.button_16x16.clicked(event):
                self.button_4x4.pressed = False
                self.button_9x9.pressed = False
                self.button_16x16.pressed = True
                self.button_25x25.pressed = False
                self.SIZE = 16
                self.BLOCK_SIZE = 35
                self.WINDOW_WIDTH = 800
                self.WINDOW_HEIGHT = 800
                self.BOX_ROWS = self.BOX_COLS = sqrt(self.SIZE)
                self.PLAY_WIDTH = self.BLOCK_SIZE * self.SIZE
                self.PLAY_HEIGHT = self.BLOCK_SIZE * self.SIZE
                self.TOP_LEFT = (
                    self.WINDOW_WIDTH // 2 - self.PLAY_WIDTH // 2,
                    self.WINDOW_HEIGHT // 2 - self.PLAY_HEIGHT // 2,
                )
            if self.button_25x25.clicked(event):
                self.button_4x4.pressed = False
                self.button_9x9.pressed = False
                self.button_16x16.pressed = False
                self.button_25x25.pressed = True
                self.SIZE = 25
                self.BLOCK_SIZE = 26
                self.WINDOW_WIDTH = 850
                self.WINDOW_HEIGHT = 850
                self.BOX_ROWS = self.BOX_COLS = sqrt(self.SIZE)
                self.PLAY_WIDTH = self.BLOCK_SIZE * self.SIZE
                self.PLAY_HEIGHT = self.BLOCK_SIZE * self.SIZE
                self.TOP_LEFT = (
                    self.WINDOW_WIDTH // 2 - self.PLAY_WIDTH // 2,
                    self.WINDOW_HEIGHT // 2 - self.PLAY_HEIGHT // 2,
                )
            if event.type == pygame.QUIT:
                # if quit button is clicked, exit the game
                pygame.quit()
                exit()

        # display the play game button
        self.button_play_game.draw(self.window)
        # display the available options
        self.button_4x4.draw(self.window)
        self.button_9x9.draw(self.window)
        self.button_16x16.draw(self.window)
        self.button_25x25.draw(self.window)

        # update the pygame display screen
        pygame.display.update()
        # return that no option is selected
        return 0

    def draw_window(self, solved: bool = False):
        """Draw the window for the game"""
        # solve button
        self.button_solve = Button(
            self.WINDOW_WIDTH // 2,
            self.WINDOW_HEIGHT - 60,
            self.PLAY_WIDTH,
            60,
            (200, 200, 200),
            "Solve",
        )

        # fill the background
        self.window.fill((255, 255, 255))
        # heading font
        font = pygame.font.SysFont("comicsans", 48)
        # heading label
        label = font.render("SUDOKU", 1, (0, 0, 0))
        # display the label
        self.window.blit(
            label,
            (
                self.TOP_LEFT[X] + self.PLAY_WIDTH / 2 - (label.get_width() / 2),
                60 - (label.get_height() / 2),
            ),
        )

        # draw reference grid black lines
        for i in range(self.SIZE):
            # horizontal lines
            pygame.draw.line(
                self.window,
                (0, 0, 0),
                (self.TOP_LEFT[X], self.TOP_LEFT[Y] + i * self.BLOCK_SIZE),
                (
                    self.TOP_LEFT[X] + self.PLAY_WIDTH,
                    self.TOP_LEFT[Y] + i * self.BLOCK_SIZE,
                ),
                4 if i % self.BOX_ROWS == 0 else 1,
            )
        for i in range(self.SIZE):
            # vertical lines
            pygame.draw.line(
                self.window,
                (0, 0, 0),
                (self.TOP_LEFT[X] + i * self.BLOCK_SIZE, self.TOP_LEFT[Y]),
                (
                    self.TOP_LEFT[X] + i * self.BLOCK_SIZE,
                    self.TOP_LEFT[Y] + self.PLAY_HEIGHT,
                ),
                4 if i % self.BOX_COLS == 0 else 1,
            )

        # last horizontal line
        pygame.draw.line(
            self.window,
            (0, 0, 0),
            (self.TOP_LEFT[X], self.TOP_LEFT[Y] + self.SIZE * self.BLOCK_SIZE),
            (
                self.TOP_LEFT[X] + self.PLAY_WIDTH,
                self.TOP_LEFT[Y] + self.SIZE * self.BLOCK_SIZE,
            ),
            4,
        )

        # last vertical line
        pygame.draw.line(
            self.window,
            (0, 0, 0),
            (self.TOP_LEFT[X] + self.SIZE * self.BLOCK_SIZE, self.TOP_LEFT[Y]),
            (
                self.TOP_LEFT[X] + self.SIZE * self.BLOCK_SIZE,
                self.TOP_LEFT[Y] + self.PLAY_HEIGHT,
            ),
            4,
        )

        # font for the numbers, with different size
        font = pygame.font.SysFont("comicsans", 23)
        # iterate through rows
        for i in range(self.SIZE):
            # iterate through columns
            for j in range(self.SIZE):
                if self.matrix[i, j] == 0:
                    continue
                if (i, j) in self.locked_pos:
                    num_color = (0, 0, 0)
                elif solved:
                    num_color = (128, 193, 42)
                elif Sudoku.element_possible(self.matrix, self.SIZE, i, j):
                    num_color = (89, 154, 252)
                else:
                    num_color = (255, 0, 0)
                label = font.render(str(self.matrix[i, j]), 1, num_color)
                self.window.blit(
                    label,
                    (
                        self.TOP_LEFT[X]
                        + j * self.BLOCK_SIZE
                        - label.get_width() / 2
                        + self.BLOCK_SIZE / 2,
                        self.TOP_LEFT[Y]
                        + i * self.BLOCK_SIZE
                        - label.get_height() / 2
                        + self.BLOCK_SIZE / 2,
                    ),
                )

        # highlight border of the selected box
        pygame.draw.rect(
            self.window,
            (100, 178, 255),
            (
                self.TOP_LEFT[X] + self.selected_box[0] * self.BLOCK_SIZE,
                self.TOP_LEFT[Y] + self.selected_box[1] * self.BLOCK_SIZE,
                self.BLOCK_SIZE,
                self.BLOCK_SIZE,
            ),
            4,
        )

        # display the home button
        self.button_home.draw(self.window)
        # display the icon on the home button
        self.window.blit(
            self.home_icon,
            (
                self.button_home.x - self.home_icon.get_width() / 2,
                self.button_home.y - self.home_icon.get_height() / 2,
            ),
        )

        # display the solve button
        self.button_solve.draw(self.window)
        pygame.display.update()

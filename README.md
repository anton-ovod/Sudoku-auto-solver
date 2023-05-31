# Python Sudoku Auto Solver with Pygame GUI

This is a Python program that solves Sudoku puzzles automatically using a backtracking algorithm and provides a graphical user interface (GUI) using the Pygame library.

## Requirements

To run this program, you need the following:

- Python 3.x: The programming language used to develop the solver.
- Pygame: The library used to create the GUI.
- Sudoku Puzzle: You can provide the Sudoku puzzle as a text file (9x9 grid), where empty cells are represented by zeros (0).

## Installation

1. Clone or download the repository to your local machine.
2. Install Python 3.x from the official Python website if you haven't already.
3. Install the Pygame library by running the following command in your terminal or command prompt:

```
pip install pygame
```

## Usage

1. Open the terminal or command prompt and navigate to the directory where you cloned or downloaded the repository.
2. Run the following command to start the Sudoku solver:

```
python sudoku_solver.py
```

3. The Pygame window will open, displaying an empty Sudoku grid.
4. To input your Sudoku puzzle, click on a cell and type the number using your keyboard. Press Enter or Return to confirm the input.
5. Once you have entered all the known numbers, press the Spacebar to start the solving process.
6. The program will automatically solve the Sudoku puzzle and display the solution on the GUI.
7. You can press the Spacebar again to clear the board and enter a new puzzle.

## How it Works

1. The program uses a backtracking algorithm to solve the Sudoku puzzle. It starts by finding an empty cell in the grid and tries different numbers from 1 to 9 in that cell.
2. If a number is valid, it moves on to the next empty cell and repeats the process. If a number is not valid, it backtracks and tries the next number.
3. This process continues until a solution is found or all possibilities are exhausted.
4. The program updates the GUI in real-time, showing the progress and the final solution.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/your-repository).

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify the code for personal or commercial purposes.

## Acknowledgements

This program was developed using the knowledge and techniques learned from various Python tutorials and resources. Special thanks to the Pygame community for creating a powerful library for building interactive applications.

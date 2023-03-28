from Sudoku_GUI import SudokuGame
import tkinter as tk
def main():
    root = tk.Tk()
    root.title("Sudoku Solver")
    game_board = SudokuGame(root, 5)
    game_board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    get_matrix_button = tk.Button(root, text="Get Matrix", command=lambda: print(game_board.get_matrix()))
    get_matrix_button.pack(side="bottom", padx=4, pady=4)
    root.mainloop()


if __name__ == "__main__":
    main()
import tkinter as tk


class SudokuGame(tk.Frame):
    def __init__(self, parent, size=5):
        tk.Frame.__init__(self, parent)
        self.board = []
        self.cols = self.size = self.rows = size
        self.grid()
        self.create_board()

    def create_board(self):
        for row in range(self.rows):
            row_data = []
            for col in range(self.cols):
                cell = tk.Label(self, text="_", font=("Arial", 30), width=2, height=1, relief="solid", borderwidth=1)
                cell.grid(row=row, column=col, padx=4, pady=4)
                cell.bind('<Button-1>', self.on_click)
                row_data.append(cell)
            self.board.append(row_data)

    def on_click(self, event):
        cell = event.widget
        row, col = self.get_coords(cell)
        text = cell.cget('text')
        if text == "_":
            entry = tk.Entry(self, font=('Arial', 20), width=2, justify='center')
            entry.grid(row=row, column=col, padx=2, pady=2)
            entry.bind("<Return>", lambda event: self.on_entry_submit(entry, row, col))
            entry.focus()
            entry.bind("<Double 1>", lambda event: self.hide_entry(entry, row, col))
        else:
            num = int(text)
            entry = tk.Entry(self, font=('Arial', 20), width=2, justify='center')
            entry.insert(0, str(num))
            entry.grid(row=row, column=col, padx=2, pady=2)
            entry.bind("<Return>", lambda event: self.on_entry_submit(entry, row, col))
            entry.bind("<Double 1>", lambda event: self.hide_entry(entry, row, col))
            entry.focus()

    def hide_entry(self, entry, row, col):
        if self.board[row][col].cget("text").isdigit():
            self.board[row][col].config(text="_")
        entry.destroy()


    def on_entry_submit(self, entry, row, col):
        num = entry.get()
        current_values = [x.cget("text") for x in self.board[row]]
        if num.isdigit() and 0 <= int(num) <= self.size and num not in current_values:
            self.board[row][col].config(text=num)
            entry.destroy()
        elif not num.isdigit() or (num.isdigit() and int(num) > self.size or int(num) < 0) or num in current_values:
            entry.config(fg='red')
        else:
            self.board[row][col].config(text='_')
            entry.destroy()

    def get_coords(self, cell) -> int:
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == cell:
                    return row, col

    def get_matrix(self):
        matrix = []
        for row in range(self.rows):
            row_data = []
            for col in range(self.cols):
                text = self.board[row][col].cget('text')
                if text.isdigit():
                    row_data.append(int(text))
                else:
                    row_data.append(0)
            matrix.append(row_data)
        return matrix

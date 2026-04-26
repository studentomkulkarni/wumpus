import random
import tkinter as tk
from tkinter import messagebox

class WumpusGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hunt the Wumpus")
        self.grid_size = 4

        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        self.info_frame = tk.Frame(self.root, padx=10, pady=10)
        self.info_frame.pack()

        self.status = tk.Label(self.info_frame, text="Find the gold. Avoid dangers!", wraplength=300)
        self.status.pack(anchor="w")

        self.hint = tk.Label(self.info_frame, text="", fg="blue")
        self.hint.pack(anchor="w", pady=5)

        self.board_frame = tk.Frame(self.root, bg="black")
        self.board_frame.pack()

        self.cells = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                lbl = tk.Label(self.board_frame, width=6, height=3, bg="white", relief="solid")
                lbl.grid(row=i, column=j, padx=2, pady=2)
                row.append(lbl)
            self.cells.append(row)

        self.control_frame = tk.Frame(self.root, pady=10)
        self.control_frame.pack()

        self.create_buttons()

    def create_buttons(self):
        self.buttons = {
            "UP": tk.Button(self.control_frame, text="↑", command=lambda: self.move_player("UP")),
            "DOWN": tk.Button(self.control_frame, text="↓", command=lambda: self.move_player("DOWN")),
            "LEFT": tk.Button(self.control_frame, text="←", command=lambda: self.move_player("LEFT")),
            "RIGHT": tk.Button(self.control_frame, text="→", command=lambda: self.move_player("RIGHT")),
            "RESTART": tk.Button(self.control_frame, text="Restart", command=self.start_new_game)
        }

        self.buttons["UP"].grid(row=0, column=1)
        self.buttons["LEFT"].grid(row=1, column=0)
        self.buttons["RIGHT"].grid(row=1, column=2)
        self.buttons["DOWN"].grid(row=2, column=1)
        self.buttons["RESTART"].grid(row=1, column=1)

    def start_new_game(self):
        self.grid = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.player = [0, 0]
        self.finished = False

        self.place_object("W")  # Wumpus
        self.place_object("G")  # Gold

        for _ in range(3):
            self.place_object("P")  # Pit

        self.refresh_board()

    def place_object(self, symbol):
        while True:
            r = random.randint(0, self.grid_size - 1)
            c = random.randint(0, self.grid_size - 1)
            if self.grid[r][c] == "" and (r, c) != (0, 0):
                self.grid[r][c] = symbol
                break

    def get_clues(self, r, c):
        clues = []
        moves = [(-1,0),(1,0),(0,-1),(0,1)]

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                if self.grid[nr][nc] == "W":
                    clues.append("Stench")
                if self.grid[nr][nc] == "P":
                    clues.append("Breeze")
                if self.grid[nr][nc] == "G":
                    clues.append("Shine")
        return clues

    def evaluate_position(self):
        r, c = self.player
        tile = self.grid[r][c]

        if tile == "W":
            return "You were eaten by the Wumpus!"
        elif tile == "P":
            return "You fell into a pit!"
        elif tile == "G":
            return "You found the treasure!"
        return None

    def refresh_board(self, reveal=False):
        clues = self.get_clues(self.player[0], self.player[1])
        result = self.evaluate_position()

        if result:
            self.status.config(text=result)
            reveal = True
        else:
            self.status.config(text="Keep exploring...")

        self.hint.config(text="Clues: " + ", ".join(clues) if clues else "No clues nearby.")

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.cells[i][j]

                if [i, j] == self.player:
                    cell.config(text="🙂", bg="#d0f0c0")
                elif reveal and self.grid[i][j] != "":
                    cell.config(text=self.grid[i][j], bg="#ffcccc")
                else:
                    cell.config(text="", bg="white")

        if result:
            self.finished = True
            messagebox.showinfo("Game End", result)

    def move_player(self, direction):
        if self.finished:
            return

        r, c = self.player

        if direction == "UP" and r > 0:
            r -= 1
        elif direction == "DOWN" and r < self.grid_size - 1:
            r += 1
        elif direction == "LEFT" and c > 0:
            c -= 1
        elif direction == "RIGHT" and c < self.grid_size - 1:
            c += 1
        else:
            self.status.config(text="Can't move there!")
            return

        self.player = [r, c]
        self.refresh_board()


# Run game
root = tk.Tk()
game = WumpusGame(root)
root.mainloop()
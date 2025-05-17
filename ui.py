# ui.py

import tkinter as tk
from game import Ship, Board

# CELL WINDOW SIZE 
CELL_SIZE = 50
# 10X10 BOARD (default)
BOARD_SIZE = 10

class BattleshipUI:
    def __init__(self, master):
        self.master = master
        self.board = Board(size=BOARD_SIZE)
        self.canvas = tk.Canvas(master, width=(BOARD_SIZE + 1)*CELL_SIZE, height=(BOARD_SIZE +1)*CELL_SIZE, bg="lightblue")
        self.canvas.pack()

        self.info_label = tk.Label(master, text="", font=("Arial", 14))
        self.info_label.pack()

        self.ship_queue = [
            ("A", 5),
            ("K", 4),
            ("M", 3), ("M", 3), 
            ("D", 2),
            ("T", 1), ("T", 1)
        ]

        self.selected_ship = None

        self.draw_grid()
        self.next_ship()

        self.drag_start = None
        self.preview_coords = []
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_board)
        self.reset_button.pack()

    def reset_board(self):
        self.board = Board()
        self.ship_queue = [
            ("A", 5),
            ("K", 4),
            ("M", 3), ("M", 3), 
            ("D", 2),
            ("T", 1), ("T", 1)
        ]
        self.selected_ship = None
        self.info_label.config(text="The game is started.")
        self.clear_preview()
        self.draw_board()
        self.next_ship()

    def on_press(self, event):
        self.clear_preview()
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE

        # Prevent interaction with header row or column
        if row == 0 or col == 0:
            self.drag_start = None
            return

        self.drag_start = (row - 1, col - 1) 

    def on_drag(self, event):
        if not self.selected_ship or not self.drag_start:
            return

        end_col = event.x // CELL_SIZE
        end_row = event.y // CELL_SIZE

        start_row, start_col = self.drag_start
        dx = end_col - start_col
        dy = end_row - start_row

        # vertical or horizontal by drag move 
        direction = "horizontal" if abs(dx) >= abs(dy) else "vertical"

        self.selected_ship.set_position(start_row, start_col, direction)
        self.preview_coords = self.selected_ship.coords
        self.show_preview()

    def on_release(self, event):
        if not self.selected_ship or not self.drag_start:
            return

        if self.board.place_ship(self.selected_ship):
            self.clear_preview()
            self.draw_board()
            self.next_ship()
        else:
            self.info_label.config(text="The wrong location. Try again!")
            self.clear_preview()

        self.drag_start = None

    def show_preview(self):
        self.canvas.delete("preview")
        for r, c in self.preview_coords:
            if 0 <= r < 10 and 0 <= c < 10:
                x0 = (c + 1) * CELL_SIZE  
                y0 = (r + 1) * CELL_SIZE  
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=2, tags="preview")

    def clear_preview(self):
        self.canvas.delete("preview")
        self.preview_coords = []

    def draw_grid(self):
        for i in range(BOARD_SIZE + 1):
            x = i * CELL_SIZE
            y_start = 0
            y_end = (BOARD_SIZE + 1) * CELL_SIZE
            self.canvas.create_line(x, y_start, x, y_end)

            y = i * CELL_SIZE
            x_start = 0
            x_end = (BOARD_SIZE + 1) * CELL_SIZE
            self.canvas.create_line(x_start, y, x_end, y)

        # Draw column numbers 1-10 (skip 0th column)
        for col in range(1, BOARD_SIZE + 1):
            x = col * CELL_SIZE + CELL_SIZE / 2
            y = CELL_SIZE / 2
            self.canvas.create_text(x, y, text=str(col), font=("Arial", 12, "bold"))

        # Draw row letters A-J (skip 0th row)
        for row in range(1, BOARD_SIZE + 1):
            x = CELL_SIZE / 2
            y = row * CELL_SIZE + CELL_SIZE / 2
            letter = chr(ord('A') + row - 1)
            self.canvas.create_text(x, y, text=letter, font=("Arial", 12, "bold"))


    def draw_board(self):
        self.canvas.delete("all")
        self.draw_grid()

        with open("boards/ships.txt", "w") as f:
            # Write column number headers
            f.write("  " + "".join(str(i + 1) for i in range(BOARD_SIZE)) + "\n")

            for r in range(BOARD_SIZE):
                line = chr(ord("A") + r) + " "  # Row label
                for c in range(BOARD_SIZE):
                    val = self.board.grid[r][c]
                    line += "-" if val == "~" else val

                    # Draw ship only if not empty
                    if val != "~":
                        x0 = (c + 1) * CELL_SIZE
                        y0 = (r + 1) * CELL_SIZE
                        x1 = x0 + CELL_SIZE
                        y1 = y0 + CELL_SIZE
                        self.canvas.create_rectangle(x0, y0, x1, y1, fill="gray", tags="ship")
                        self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=val, fill="white", font=("Arial", 10), tags="ship")

                f.write(line + "\n")

    def next_ship(self):
        if self.ship_queue:
            name, size = self.ship_queue.pop(0)
            self.selected_ship = Ship(size, name)
            self.info_label.config(text=f"Locate {size}-({name}) ship!")
        else:
            self.selected_ship = None
            self.info_label.config(text="All ships are located!")

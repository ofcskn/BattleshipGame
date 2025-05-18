import threading
import tkinter as tk
from client import GameClient
from game import Ship, Board
from protocol.commands import CLIENT_COMMAND_ATTACK_TURN, CLIENT_COMMAND_FIND_OPPONENT, CLIENT_COMMAND_OPPONENT_RIGHT_TO_ATTACK
from protocol.protocol_message import ProtocolMessage
from utils import send_json

# CELL WINDOW SIZE 
CELL_SIZE = 50
# 10X10 BOARD (default)
BOARD_SIZE = 10

class BattleshipUI:
    def __init__(self, master, client:GameClient):
        self.master = master
        self.client = client
        self.board = Board(size=BOARD_SIZE)
        self.canvas = tk.Canvas(master, width=(BOARD_SIZE)*CELL_SIZE, height=(BOARD_SIZE)*CELL_SIZE, bg="lightblue")
        self.canvas.pack()

        self.info_label2 = tk.Label(master, text=f"Location mode {self.client.addr}", font=("Arial", 14))
        self.info_label2.pack()

        self.info_label = tk.Label(master, text=f"Location mode {self.client.addr}", font=("Arial", 14))
        self.info_label.pack()

        self.score_label = tk.Label(master, text=f"The score is {self.client.get_score()}", font=("Arial", 14))
        self.score_label.pack()

        self.drag_start = None
        self.preview_coords = []
        self.selected_ship = None

        self.canvas.tag_lower("ship")  # ships at bottom
        self.canvas.tag_raise("grid")  # grid lines on top

        self.ship_queue = [
            ("A", 5),
            ("K", 4),
            ("M", 3), ("M", 3), 
            ("D", 2),
            ("T", 1), ("T", 1)
        ]

        self.draw_grid()

        # Game modes
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_board)
        self.reset_button.pack()

        self.find_match_button = tk.Button(master, text="Lets match", command=self.search_for_match)
        self.find_match_button.pack()
        self.find_match_button.config(state="disabled")

        self.next_ship()

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def reset_board(self, gameMode="1"):
        self.board = Board(gameMode, size=BOARD_SIZE)
        if self.board.gameMode == "1":
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
        else:
            self.board.gameMode = "2"
            opponent_addr = self.client.opponent_addr
            self.info_label.config(text=f"The attack mode is started. The attacker is {opponent_addr}")
            self.clear_preview()
            self.draw_board()

    def on_press(self, event):
        self.did_drag = False
        x = event.x // CELL_SIZE # row 
        y = event.y // CELL_SIZE # col

        if self.board.gameMode == "1":
            self.clear_preview()

            # if x == 0 or y == 0:
            #     self.drag_start = None
            #     return

            self.drag_start = (x, y)
            self.did_drag = False  # Track if the user dragged or not

            if self.selected_ship and self.selected_ship.size == 1:
                self.selected_ship.set_position(x, y, "horizontal")
                self.preview_coords = self.selected_ship.coords
                self.show_preview()
        else:
            if not self.client.turn:
                self.info_label.config(text=f"Not your turn or already attacked")
                return

            if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                if (x, y) in self.board.attacked_locations:
                    self.info_label.config(text="The location is attacked before.")
                    return
             
                message = ProtocolMessage(CLIENT_COMMAND_ATTACK_TURN, {"attack_x": x, "attack_y": y , "opponent_addr": self.client.opponent_addr})
                send_json(self.client.conn, message)
            
                if self.client.attacked_block_event:
                    result = self.board.attack(x, y, self.client)
                    self.draw_board()
                    if result.get("hit") == True:
                        self.score_label.config(text=f"The score is {self.client.increase_score()}")
                        message = ProtocolMessage(CLIENT_COMMAND_OPPONENT_RIGHT_TO_ATTACK, {"right": False, "opponent_addr": self.client.opponent_addr})
                        send_json(self.client.conn, message)
                        self.client.turn = True
                        self.info_label.config(text="🎯 Hit! Bomb again.")
                    else:
                        self.info_label.config(text="💨 Missed! Opponent's turn.")
            else:
                self.info_label.config(text=f"Wrong location to click!")

    def on_drag(self, event):
        self.did_drag = True
        if self.board.gameMode == "1":
            if not self.selected_ship or not self.drag_start:
                return

            self.did_drag = True  # Drag actually happened

            end_x = event.x // CELL_SIZE
            end_y = event.y // CELL_SIZE

            start_x, start_y = self.drag_start
            dx = end_x - start_x
            dy = end_y - start_y

            direction = "horizontal" if abs(dx) >= abs(dy) else "vertical"

            self.selected_ship.set_position(start_x, start_y, direction)
            self.preview_coords = self.selected_ship.coords

            self.show_preview()
        else:
            pass

    def on_release(self, event):
        if self.board.gameMode == "1":
            if not self.selected_ship or not self.drag_start:
                return

            # Only allow placement if it was a valid drag, or a size-1 click
            if self.did_drag or (self.selected_ship.size == 1):
                if self.board.place_ship(self.selected_ship):
                    self.clear_preview()
                    self.draw_board()
                    self.selected_ship = None
                    self.next_ship()
                else:
                    self.info_label.config(text="The wrong location. Try again!")
                    self.clear_preview()
            else:
                self.clear_preview()  # Clean up if user clicked with invalid ship

            self.drag_start = None

    def show_preview(self):
        if self.board.gameMode == "1":
            self.canvas.delete("preview")
            for x, y in self.preview_coords:
                if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
                    x0 = x * CELL_SIZE  
                    y0 = y * CELL_SIZE  
                    x1 = x0 + CELL_SIZE
                    y1 = y0 + CELL_SIZE
                    self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=2, tags="preview")
        else:
            print("select square preview on mode 2")
            # self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", width=2, tags="preview")

    def clear_preview(self):
        self.canvas.delete("preview")
        self.preview_coords = []

    def draw_grid(self):
        for i in range(BOARD_SIZE):
            x = i * CELL_SIZE
            y_start = 0
            y_end = (BOARD_SIZE) * CELL_SIZE
            self.canvas.create_line(x, y_start, x, y_end)

            y = i * CELL_SIZE
            x_start = 0
            x_end = (BOARD_SIZE) * CELL_SIZE
            self.canvas.create_line(x_start, y, x_end, y)

        # # Draw column numbers 1-10 (skip 0th column)
        # for col in range(1, BOARD_SIZE + 1):
        #     x = col * CELL_SIZE + CELL_SIZE / 2
        #     y = CELL_SIZE / 2
        #     self.canvas.create_text(x, y, text=str(col), font=("Arial", 14, "bold"))

        # # Draw row letters A-J (skip 0th row)
        # for row in range(1, BOARD_SIZE + 1):
        #     x = CELL_SIZE / 2
        #     y = row * CELL_SIZE + CELL_SIZE / 2
        #     letter = chr(ord('A') + row - 1)
        #     self.canvas.create_text(x, y, text=letter, font=("Arial", 14, "bold"))

    def draw_board(self):
        self.canvas.delete("all")
        self.draw_grid()

        if self.board.gameMode == "1":
            with open(f"boards/ships-{self.client.addr}.txt", "w") as f:
                # Write column number headers
                f.write("  " + "".join(str(i + 1) for i in range(BOARD_SIZE)) + "\n")

                for col in range(BOARD_SIZE):
                    line = chr(ord("A") + col) + " "  # Row label
                    for row in range(BOARD_SIZE):
                        val = self.board.grid[row][col]
                        line += "-" if val == "~" else val

                        # Draw ship only if not empty
                        if val != "~":
                            x0 = row  * CELL_SIZE
                            y0 = col  * CELL_SIZE
                            x1 = x0 + CELL_SIZE
                            y1 = y0 + CELL_SIZE
                            self.canvas.create_rectangle(x0, y0, x1, y1, fill="gray", tags="ship")
                            self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=val, fill="white", font=("Arial", 10), tags="ship")

                    f.write(line + "\n")

        elif self.board.gameMode == "2":
            with open(f"boards/daim-{self.client.addr}.txt", "w") as f:
                f.write("  " + "".join(str(i + 1) for i in range(BOARD_SIZE)) + "\n")

                for x in range(BOARD_SIZE):
                    line = chr(ord("A") + x) + " "
                    for y in range(BOARD_SIZE):
                        val = self.board.grid[x][y]
                        line += "-" if val == "~" else val

                        if val in ["X", "O", "~"]:
                            if val == "~":
                                continue
                            fill = "red" if val == "X" else "white"

                            x0 = x * CELL_SIZE
                            y0 = y * CELL_SIZE
                            x1 = x0 + CELL_SIZE
                            y1 = y0 + CELL_SIZE

                            self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, tags="attack")
                            self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=val, fill="black", font=("Arial", 10), tags="attack")
                    f.write(line + "\n")

    def next_ship(self):
        if self.ship_queue:
            name, size = self.ship_queue.pop(0)
            self.selected_ship = Ship(size, name)
            self.info_label.config(text=f"Locate {size}-({name}) ship!")
        else:
            self.selected_ship = None
            self.info_label.config(text="All ships are located!")
            # Disable the button and start search in a thread
            self.find_match_button.config(state="disabled")
            threading.Thread(target=self.search_for_match, daemon=True).start()

    def search_for_match(self, timeout=30):
        # if the board is ready to match
        if self.ship_queue or self.board.gameMode != "1":
            self.info_label.after(0, lambda: self.find_match_button.config(state="normal"))
            return 
        
        self.reset_button.config(state="disabled")
        self.info_label.config(text=f"...sarching an opponent...")
        grouped_coords = [ship.coords for ship in self.board.ships]
        message = ProtocolMessage(CLIENT_COMMAND_FIND_OPPONENT, {"isMatching": True, "inGame": False, "ships": grouped_coords})
        send_json(self.client.conn, message)

        found = self.client.match_found_event.wait(timeout=timeout)

        def after_match():
            if found:
                opponent_info = self.client.match_payload
                print(f"✅ Opponent found: {opponent_info['opponent_addr']}")
                print(f"✅ Opponent ships are: {opponent_info['opponent_ships']}")
                
                # lets change the game mode
                self.reset_board("2")
                self.find_match_button.pack_forget()

                return True
            else:
                print("❌ Timeout: No opponent found after 30 seconds.")
                # Re-enable the match button
                self.find_match_button.config(state="normal")

        # Ensure GUI updates run on the main thread
        self.info_label.after(0, after_match)
import os

AIMS_FILENAME="aim.txt"
SHIPS_FILENAME="ships.txt"

class TextBasedBattleship:
    def __init__(self, username):
        # get an username to classify players 
        self.username = username
        # ship boards 10x10 
        self.ship_board = [[" "]*10 for _ in range(10)]
        # aim boards 10x10
        self.aim_board = [[" "]*10 for _ in range(10)]
        # Ship Types 
        #(A for each) one 5 places long,(you need to ask 5 coordinates)
        # (B for each) one 4 places long,(you need to ask 4 coordinates)
        # (C for each)two 3 places long,(you need to ask 3 coordinates)
        # (D for each)two 2 places long,(you need to ask 2 coordinates)
        # (E for each) Three 1 place long ships. (you need to ask 1 coordinate)
        self.ship_types = {
            "A": (1, 5),   # one 5 places long
              "B": (1, 4),  # one 4 places long
              "C": (2, 3),  # two 3 places long
                "D": (2, 2),  # two 2 places long
            "E": (3, 1)   # Three 1 place long 
        }

    def save_board(self, filename, board, username=None):
        os.makedirs("boards", exist_ok=True)
        username = self.username if username is None else username
        board_path = f"boards/{username}_{filename}"
        # Save aims or ships boards to "boards" folder. 
        with open(board_path, "w") as f:
            # Add 1 to 10 numbers to the header
            f.write("   " + " ".join([str(i + 1).rjust(2) for i in range(10)]) + "\n")
            for i, row in enumerate(board):
                row_label = chr(65 + i)
                # Add A to J strings to the starting of the rows 
                f.write(row_label + "  " + " ".join(cell.rjust(2) for cell in row) + "\n")

    def place_ships(self):
        for ship_type, (count, size) in self.ship_types.items():
            for i in range(count):
                print(f"{self.username} placing ship type {ship_type} (size {size}), {count - i} remaining")
                while True:
                    coords = []
                    print(f"Please enter {size} coordinates (e.g., A5), separated by space:")
                    input_str = input(f"Enter {size} coordinates: ").strip().upper()
                    parts = input_str.split()
                    if len(parts) != size:
                        print(f"You must enter exactly {size} coordinates.")
                        continue
                    
                    # Check the coordinates
                    valid = True
                    for p in parts:
                        if len(p) < 2 or len(p) > 3:
                            valid = False
                            break
                        row_char, col_str = p[0], p[1:]
                        if row_char < 'A' or row_char > 'J' or not col_str.isdigit():
                            valid = False
                            break
                        row = ord(row_char) - 65
                        col = int(col_str) - 1
                        if not (0 <= row < 10 and 0 <= col < 10):
                            valid = False
                            break
                        if self.ship_board[row][col] != " ":
                            print(f"Space {p} already occupied.")
                            valid = False
                            break
                        coords.append((row, col))

                    if not valid:
                        print("Invalid coordinates. Try again.")
                        continue

                    # Place the ships to the file.
                    for r, c in coords:
                        self.ship_board[r][c] = ship_type
                    self.save_board(SHIPS_FILENAME, self.ship_board)
                    break


    def shot(self, opponent):
        while True:
            opponent_board = opponent.ship_board

            row, col = self.get_target()

            target_cell = opponent_board[row][col]

            if target_cell not in [" ", "X"]:
                print("Hit")
                self.aim_board[row][col] = "X"
                opponent_board[row][col] = "X"
                self.save_board(AIMS_FILENAME, self.aim_board)
                opponent.save_board(SHIPS_FILENAME, opponent_board)
                opponent.ship_board = opponent_board

                print(f"{self.username}'s Aim Board:")
                self.print_board(self.aim_board)

                if self.check_win(opponent_board):
                    print(f"{self.username} win the game!")
                    return True  

                continue  # Hit again
            elif target_cell == "X" or self.aim_board[row][col] in ["X", "O"]:
                print("Already targeted this location")
            else:
                print("Miss")
                self.aim_board[row][col] = "O"
                self.save_board(AIMS_FILENAME, self.aim_board, self.username)
                print(f"{self.username}'s Aim Board:")
                self.print_board(self.aim_board)
                return False 

    def print_board(self, board):
        # show the board
        for i, row in enumerate(board):
            row_label = chr(65 + i)
            print(row_label + "  " + " ".join(cell.rjust(2) for cell in row))

    def get_target(self):
        while True:
            target = input(f"{self.username}, enter target (B7, a2, c3):").strip().upper()
            if len(target) < 2 or len(target) > 3:
                print("Invalid format")
                continue
            row_char, col_str = target[0], target[1:]
            if row_char < 'A' or row_char > 'J' or not col_str.isdigit():
                print("Invalid input.")
                continue
            row = ord(row_char) - 65
            col = int(col_str) - 1
            if not (0 <= row < 10 and 0 <= col < 10):
                print("Out of size.")
                continue
            return row, col

    def check_win(self, opponent_board):
        # Check if all ship parts on the opponent's board are hit in the user's aim board
        for i in range(10):
            for j in range(10):
                cell = opponent_board[i][j]
                if cell in self.ship_types:  # If there's a ship part
                    if self.aim_board[i][j] != "X":
                        return False  # This ship cell hasn't been hit yet
        return True

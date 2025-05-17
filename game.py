class Ship:
    def __init__(self, size, name):
        # Ship sizes can be 5, 4, 3, 2, 1
        self.size = size
        # Name of the ship is located on the board (A, K, M, D, T)
        self.name = name
        # coordinates of the ship
        self.coords = []
        # as a game rule, every ship can be located as horizontal or vertical (not cross)
        self.direction = 'horizontal'

    def set_position(self, start_row, start_col, direction):
        self.direction = direction
        self.coords = []
        for i in range(self.size):
            if direction == 'horizontal':
                self.coords.append((start_row, start_col + i))
            else:
                self.coords.append((start_row + i, start_col))

class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [["~"] * size for _ in range(size)]
        self.ships = []

    def is_valid_position(self, ship):
        for row, col in ship.coords:
            if row < 0 or col < 0 or row >= self.size or col >= self.size:
                return False
            if self.grid[row][col] != "~":
                return False
        return True

    def place_ship(self, ship):
        if self.is_valid_position(ship):
            for row, col in ship.coords:
                self.grid[row][col] = ship.name
            self.ships.append(ship)
            return True
        return False

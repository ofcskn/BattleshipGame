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

    def set_position(self, start_x, start_y, direction):
        self.direction = direction
        self.coords = []
        for i in range(self.size):
            if direction == 'vertical':
                self.coords.append((start_x, start_y + i))
            else:
                self.coords.append((start_x + i, start_y))
    
    def to_dict(self):
        return {
            "name": self.name,
            "size": self.size,
            "direction": self.direction,
            "coords": self.coords
        }

class Board:
    def __init__(self, gameMode="1", size=10):
        self.size = size
        self.grid = [["~"] * size for _ in range(size)]
        self.ships = []
        self.attacked_locations = set()  # Use a set for quick lookup
        self.gameMode = gameMode

    def is_valid_position(self, ship):
        return all(
            0 <= x < self.size and
            0 <= y < self.size and
            self.grid[x][y] == "~"
            for x, y in ship.coords
        )

    def place_ship(self, ship):
        if self.is_valid_position(ship):
            for x, y in ship.coords:
                self.grid[x][y] = ship.name
            self.ships.append(ship)
            return True
        return False

    def attack(self, x, y, client):
        if client.turn == False:
            return { "hit": False, "error": "noTurn", "attacked_locations": self.attacked_locations }
        if (x, y) in self.attacked_locations:
            return { "hit": False, "error": "attackedBefore", "attacked_locations": self.attacked_locations }
        self.attacked_locations.add((x, y))
        for opponentShip in client.opponent_ships:
            for shipLocation in opponentShip:
                if [x, y] == shipLocation:
                    self.grid[x][y] = "X"
                    client.turn = True
                    return { "hit": True, "attacked_locations": self.attacked_locations }
        
        self.grid[x][y] = "O"
        return { "hit": False, "attacked_locations": self.attacked_locations }
# BattleshipGame

The Battleship tabletop game is a classic strategic naval combat game designed for two players.

---

## Setup Virtual Environment

### On Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### On Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

To deactivate the virtual environment:

```bash
deactivate
```

---

## Requirements

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

---

## Run the Project

Once the environment is active, start the application with:

```bash
python main.py
```

For Board&Socket-Based (GUI based) game, start the server.

```bash
python server.py
```

---

# GAMES

There are two games: **Text-Based Battleship** or **Board&Socket-Based Battleship**

## Text-Based Battleship Game

A two-player Battleship game played directly in the terminal! Players take turns placing ships and firing shots to sink each other's fleet. The first player to sink all opponent ships wins.

---

### Rules

1. The game is played on a **10x10 grid** (A-J rows, 1-10 columns).
2. Each player has two boards:

   - **Ship Board**: Where they place their ships.
   - **Aim Board**: Where they track their shots at the opponent.

3. Players **take turns**:

   - Choose a coordinate to **attack** (e.g., `B5`).
   - If it's a **hit**, you shoot again.
   - If it's a **miss**, your turn ends.

4. The first player to **hit all parts of the opponent’s ships** wins.

---

### Ship Types (ship_types)

| Symbol | Quantity | Size |
| ------ | -------- | ---- |
| A      | 1        | 5    |
| B      | 1        | 4    |
| C      | 2        | 3    |
| D      | 2        | 2    |
| E      | 3        | 1    |

> You will be asked to input coordinates for each ship. For example, a 3-cell ship must be placed as `A1 a2 a3` (horizontally) or `B5 c5 d5` (vertically).

---

### How to Play

1. **Run main.py** in your terminal.

```bash
python main.py
```

2. **Select Text-based game mode. Write 1 to start the game**

```bash
    Select game mode:
    1 - Text-based
    2 - GUI-based
    Enter choice:
```

3. **Each player enters their username. The usernames cannot be same.**.
4. **Place your ships. Follow the terminal constructions.**:

   - Input exact number of coordinates per ship.
   - Ships must be in a straight, **contiguous line**.
   - Ships **cannot overlap**.

5. **Start the battle**:

   - On your turn, enter a coordinate like `C7` or `d7`.
   - You’ll see a `username's Aim Board` `Hit ` or `Miss`
   - Hits allow extra turns.
   - Boards are saved between turns.

6. **Victory Condition**:

   - If all opponent ships are hit (based on ship types and sizes), you win.

---

### Saved Boards

- Your boards are saved in a `/boards` folder as text files. Filenames can be changed by `AIMS_FILENAME` and `SHIPS_FILENAME` in constants.
- Examples:

  - `username_ships.txt`
  - `username_aims.txt`

---

### Input/Output Example

```bash
username1, enter enter target (B7, a2, c3) B5
- Hit
Hit again!

username2, enter target (B7, a2, c3): C9
- Miss
```

---

## Board&Socket-Based Battleship

A two-player Battleship board game played with boards! Players place ships and find match. Then shots to sink each other's fleet. The first player to sink all opponent ships wins.

---

### Rules

1. The game is played on a **10x10 grid board** (A-J rows, 1-10 columns) (not yet).
2. Each player has two boards:

   - **Ship Board**: Where they place their ships.
   - **Aim Board**: Where they track their shots at the opponent.

3. Players **take turns**:

   - Click a coordinate on the board to **attack** (e.g., `B5`).
   - If it's a **hit**, you shoot again. You will see red filled `X` block.
   - If it's a **miss**, your turn ends. You will see white filled `O` block.

4. The first player to **hit all parts of the opponent’s ships** wins.

---

### Ship Types (ship_types)

| Symbol | Quantity | Size |
| ------ | -------- | ---- |
| A      | 1        | 5    |
| B      | 1        | 4    |
| C      | 2        | 3    |
| D      | 2        | 2    |
| E      | 3        | 1    |

### Protocol

[PROTOCOL DOCUMENT](/protocol/PROTOCOL.MD)

### How to Play

1. **Run the server.py** in your terminal.

```bash
python server.py
```

2. **Run main.py** in other terminals. Every player (client) needs to start in another terminal.

```bash
python main.py
```

3. **Select GUI-based game mode. Write 2 to start the game**

```bash
    Select game mode:
    1 - Text-based
    2 - GUI-based
    Enter choice:
```

4. **Place your ships on the board. You will see preview of the ships.**:

   - Ships must be in a straight, **contiguous line**.
   - Ships **cannot overlap**.
   - Ships can be located **horizontally or vertically**.

5. **Find an opponent by waiting players in the server.**:

   - You’ll see a label when you hit or miss.
   - Hits allow extra turns.
   - Boards are saved between turns.

6. **Victory Condition**:

   - If all opponent ships are hit (based on ship types and sizes), you win.

---

## Contact

For questions or support, feel free to contact:

**Ömer Faruk COŞKUN**
[info@ofcskn.com](mailto:info@ofcskn.com)
[ofcskn.com](https://ofcskn.com)

```

```

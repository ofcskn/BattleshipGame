import tkinter as tk
from client import GameClient
from ui import BattleshipUI

def main():
    root = tk.Tk()
    root.title("Battleship Game Board")

    # Listen the client socket
    client = GameClient()
    client.handle_client()

    BattleshipUI(root, client)
    root.mainloop()

if __name__ == "__main__":
    main()

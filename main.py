import tkinter as tk
from client import GameClient
from ui import BattleshipUI

def main():
    root = tk.Tk()
    root.title("Battleship Game Board")

    # Listen the client socket
    client = GameClient()
    client.handle_client()

    app = BattleshipUI(root, client)
    root.mainloop()

    input("Press Enter to exit...\n")
    client.stop_listening()

if __name__ == "__main__":
    main()

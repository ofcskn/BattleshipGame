import tkinter as tk
from ui import BattleshipUI

def main():
    root = tk.Tk()
    root.title("BattleshipGame Board")
    app = BattleshipUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

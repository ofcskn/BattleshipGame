import os
import tkinter as tk
from client import GameClient
from text_game import TextBasedBattleship
from ui import BattleshipUI
import tkinter as tk

def main():
    game_mode = input("Select game mode:\n1 - Text-based\n2 - GUI-based\nEnter choice: ")
    os.makedirs("boards", exist_ok=True)

    match game_mode:
        case "1":
            # with text
            print("Welcome to Text-Based Battleship!\n")

            # Get player1 username and create TextBasedBattleship
            username1 = input("Enter username for Player 1: ").strip()
            player1 = TextBasedBattleship(username1)
            player1.place_ships()

            # The usernames cannot be same to prevent conflicts in filenames
            isUsernameUnique = False
            while (not isUsernameUnique):
                # Get player 2username and create TextBasedBattleship
                username2 = input("\nEnter username for Player 2: ").strip()
                isUsernameUnique = True if username1 != username2 else False
                print("Your username cannot be same with your opponent's username.")

            player2 = TextBasedBattleship(username2)
            player2.place_ships()

            print("Ship placement completed. Starting the battle!")

            current_player, opponent = player1, player2
            while True:
                print(f"{current_player.username}'s turn to shoot!")
                hit_again = current_player.shot(opponent)
                if hit_again is True:
                    print(f"{current_player.username} wins the game!")
                    break
                current_player, opponent = opponent, current_player
        case "2":
            # with GUI
            root = tk.Tk()
            root.title("Battleship Game Board")

            try:
                client = GameClient()
                client.handle_client()

                BattleshipUI(root, client)
                root.mainloop()
            except ConnectionRefusedError as e:
                print(e)
                print("Please start server.py")

        case _:
            print("Invalid choice. Exiting.")
            return

if __name__ == "__main__":
    main()

import socket
import threading
from constants import HOST, PORT
from protocol.commands import SERVER_COMMAND_ATTACK_BLOCK, SERVER_COMMAND_FOUND_OPPONENT, SERVER_COMMAND_LEFT_MATCH, SERVER_COMMAND_NOT_MATCHED, SERVER_COMMAND_OPPONENT_IS_ATTACKED_BLOCK, SERVER_COMMAND_OPPONENT_RIGHT_TO_ATTACK, SERVER_COMMAND_RIGHT_TO_ATTACK
from utils import recv_json, send_json

class GameClient:
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((HOST, PORT))
        self.listening = False
        self.addr = self.conn.getsockname()
        self.opponent_addr = None
        self.opponent_ships = None
        self.match_found_event = threading.Event()
        self.match_payload = None 
        self.attacked_block_event = threading.Event()
        self.attacked_x = None
        self.attacked_y = None
        self.turn = True
        self.score = 0 
        self.restart_event = threading.Event()
    
    def increase_score(self):
        self.score = self.score + 1
        return self.score

    def get_score(self):
        return self.score 

    def handle_client(self):
        def listen():
            print(f"Listening to the client server... {self.addr}")
            while self.listening:
                try:
                    message = recv_json(self.conn)
                    if not message:
                        print("Server disconnected.")
                        break
                    # Handle commands from the server
                    command = message.command
                    if command == SERVER_COMMAND_FOUND_OPPONENT:
                        self.match_payload = message.payload
                        self.opponent_addr = message.payload.get("opponent_addr")
                        self.opponent_ships = message.payload.get("opponent_ships")
                        self.match_found_event.set()
                    elif command == SERVER_COMMAND_ATTACK_BLOCK:
                        self.opponent_addr = message.payload.get("opponent_addr")
                        print(f"You {self.addr} attack to {self.opponent_addr}.")
                        self.attacked_x = message.payload.get("attack_x")
                        self.attacked_y = message.payload.get("attack_y")
                        print(f"Your attack's location is {self.attacked_x}, {self.attacked_y}.")
                        self.attacked_block_event.set()
                        self.turn = False
                    elif command == SERVER_COMMAND_OPPONENT_IS_ATTACKED_BLOCK:
                        self.opponent_addr = message.payload.get("opponent_addr")
                        print(f"The attacker {self.opponent_addr} is attacked you.")
                        self.attacked_x = message.payload.get("attack_x")
                        self.attacked_y = message.payload.get("attack_y")
                        print(f"The attack location is {self.attacked_x}, {self.attacked_y}.")
                        self.attacked_block_event.set()
                        self.turn = True
                    elif command == SERVER_COMMAND_RIGHT_TO_ATTACK:
                        self.turn = message.payload.get("right")
                    elif command == SERVER_COMMAND_OPPONENT_RIGHT_TO_ATTACK:
                        self.turn = message.payload.get("right")
                    elif command == SERVER_COMMAND_NOT_MATCHED:
                        self.match_found_event.clear()
                        print("The opponent is not found.")
                    elif command == SERVER_COMMAND_LEFT_MATCH:
                        print("The opponent left from the match.")
                        self.restart_event.set()
                except Exception as e:
                    print(f"Error while listening to server: {e}")
                    break
            self.conn.close()

        self.listening = True
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

    def stop_listening(self):
        self.listening = False

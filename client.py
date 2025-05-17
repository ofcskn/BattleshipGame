import socket
import threading
from constants import HOST, PORT
from protocol.commands import SERVER_COMMAND_FOUND_OPPONENT, SERVER_COMMAND_NOT_MATCHED
from protocol.protocol_message import ProtocolMessage

class GameClient:
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((HOST, PORT))
        self.listening = False
        self.match_found_event = threading.Event()
        self.match_payload = None  # To store matched opponent info

    def send(self, message: ProtocolMessage):
        self.conn.sendall(message.encode())

    def handle_client(self):
        def listen():
            print("Listening to the client server...")
            while self.listening:
                try:
                    response = self.conn.recv(4096)
                    if not response:
                        print("Server disconnected.")
                        break
                    message = ProtocolMessage.decode(response)
                    # Handle commands from the server
                    command = message.command
                    if command == SERVER_COMMAND_FOUND_OPPONENT:
                        print("Opponent found!", message.payload)
                        self.match_payload = message.payload
                        self.match_found_event.set()
                    elif command == SERVER_COMMAND_NOT_MATCHED:
                        self.match_found_event.clear()
                        print("The opponent is not found.")
                except Exception as e:
                    print(f"Error while listening to server: {e}")
                    break
            self.conn.close()

        self.listening = True
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

    def stop_listening(self):
        self.listening = False

import socket
import threading
from constants import HOST, PORT
from protocol.protocol_message import ProtocolMessage

class GameClient:
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((HOST, PORT))
        self.username = None
        self.listening = False

    def set_user(self, username):
        self.username = username

    def get_user(self):
        return self.username

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
                    print(f"[Server] {message.command}: {message.payload}")
                except Exception as e:
                    print(f"Error while listening to server: {e}")
                    break
            self.conn.close()

        self.listening = True
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

    def stop_listening(self):
        self.listening = False

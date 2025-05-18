import socket
import threading
from constants import HOST, PORT
from handler import handle_client

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)
print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

players = {}
waiting_players = []  # List of players are waiting to match

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr, players, waiting_players))
    thread.start()
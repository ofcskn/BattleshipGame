
from protocol.commands import CLIENT_COMMAND_FIND_OPPONENT, SERVER_COMMAND_FOUND_OPPONENT, SERVER_COMMAND_NOT_MATCHED
from protocol.protocol_message import ProtocolMessage

players = {}
waiting_players = []  # List of players are waiting to match

def handle_client(conn, addr):    
    with conn:
        print(f"[+] [NEW CONNECTION] {addr} connected.")
        players[conn] = { "address": addr, "opponentAddress": None, "inGame": False, "isMatching": False}

        while True:
            try:
                # Decode the data with Protocol Message
                data = ProtocolMessage.decode(conn.recv(1024))
                if not data:
                    break
                print(f"[RECEIVED] {addr}: {data}")

                # COMMANDS FROM CLIENT
                command = data.command
                if command == CLIENT_COMMAND_FIND_OPPONENT:
                    try_to_match(conn)
                else:
                    message = ProtocolMessage(SERVER_COMMAND_NOT_MATCHED, {"address": addr})
                    conn.sendall(message.encode()) 
            except:
                print(f"[-] [ERROR] {addr}")
                break
    
    print(f"[-] [DISCONNECT] {addr}")
    conn.close()

def try_to_match(current_conn):
    if waiting_players:
        opponent_conn = waiting_players.pop(0)

        # Match both
        players[current_conn]["inGame"] = True
        players[opponent_conn]["inGame"] = True

        players[current_conn]["isMatching"] = False
        players[opponent_conn]["isMatching"] = False

        addr1 = players[current_conn]["address"]
        addr2 = players[opponent_conn]["address"]

        # Notify both
        current_conn.sendall(ProtocolMessage(SERVER_COMMAND_FOUND_OPPONENT, {"opponentAddress": addr2}).encode())
        opponent_conn.sendall(ProtocolMessage(SERVER_COMMAND_FOUND_OPPONENT, {"opponentAddress": addr1}).encode())
        print(f"Matched {addr1} with {addr2}")
    else:
        # No opponent yet, add to waiting list
        waiting_players.append(current_conn)
        print(f"{players[current_conn]['address']} is waiting for opponent...")

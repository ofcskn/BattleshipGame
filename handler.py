
from protocol.commands import CLIENT_COMMAND_ATTACK_TURN, CLIENT_COMMAND_FIND_OPPONENT, SERVER_COMMAND_ATTACK_BLOCK, SERVER_COMMAND_FOUND_OPPONENT, SERVER_COMMAND_NOT_MATCHED, SERVER_COMMAND_OPPONENT_IS_ATTACKED_BLOCK
from protocol.protocol_message import ProtocolMessage
from utils import recv_json, send_json

def handle_client(conn, addr, players, waiting_players):    
    with conn:
        print(f"[+] [NEW CONNECTION] {addr} connected.")
        players[conn] = { "address": addr, "opponent_addr": None, "inGame": False, "isMatching": False, "ships": []}

        while True:
            try:
                data = recv_json(conn)

                if not data:
                    break
                # COMMANDS FROM CLIENT
                command = data.command
                if command == CLIENT_COMMAND_FIND_OPPONENT:
                    # Located ships of the player
                    players[conn]["ships"] = data.payload.get("ships")
                    if waiting_players:
                        opponent_conn = waiting_players.pop(0)

                        # Match both
                        players[conn]["inGame"] = True
                        players[opponent_conn]["inGame"] = True

                        players[conn]["isMatching"] = False
                        players[opponent_conn]["isMatching"] = False

                        addr1 = players[conn]["address"]
                        addr2 = players[opponent_conn]["address"]

                        players[conn]["opponent_addr"] = addr2
                        players[opponent_conn]["opponent_addr"] = addr1

                        # Notify both
                        send_json(conn, ProtocolMessage(SERVER_COMMAND_FOUND_OPPONENT, {"opponent_addr": addr2, "opponent_ships": players[opponent_conn]["ships"]}))
                        send_json(opponent_conn, ProtocolMessage(SERVER_COMMAND_FOUND_OPPONENT, {"opponent_addr": addr1, "opponent_ships": players[conn]["ships"]}))
                        print(f"Matched {addr1} with {addr2}")
                    else:
                        # No opponent yet, add to waiting list
                        waiting_players.append(conn)
                        print(f"{players[conn]['address']} is waiting for opponent...")
                elif command == CLIENT_COMMAND_ATTACK_TURN and players[conn]["opponent_addr"] != None:
                    attack_x = data.payload.get("attack_x")
                    attack_y = data.payload.get("attack_y")
                    opponent_addr = tuple(data.payload.get("opponent_addr"))

                    opponent_conn = None
                    for connection, info in players.items():
                        print(connection, info)
                        print(info["address"])
                        if info["address"] == opponent_addr:
                            opponent_conn = connection
                            break

                    if opponent_conn:
                        send_json(opponent_conn, ProtocolMessage(
                            SERVER_COMMAND_OPPONENT_IS_ATTACKED_BLOCK,
                            {
                                "attack_y": attack_y,
                                "attack_x": attack_x,
                                "opponent_addr": addr 
                            }
                        ))
                    else:
                        print(f"Opponent address {opponent_addr} not found in players: {[info['address'] for info in players.values()]}")
                    print("SERVER_COMMAND_ATTACK_BLOCK")
                    send_json(conn, ProtocolMessage(SERVER_COMMAND_ATTACK_BLOCK, {"attack_y": attack_y, "attack_x": attack_x, "opponent_addr": opponent_addr}))
                else:
                    message = ProtocolMessage(SERVER_COMMAND_NOT_MATCHED, {"address": addr})
                    send_json(conn, message)
            except:
                print(f"[-] [ERROR] {addr}")
                break
    
    print(f"[-] [DISCONNECT] {addr}")
    players.pop(conn, None)  # removes it if exists, does nothing otherwise (when the player disconnects)
    conn.close()

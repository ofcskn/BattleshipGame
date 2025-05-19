
from protocol.commands import CLIENT_COMMAND__CANCEL_FIND_OPPONENT, CLIENT_COMMAND_ATTACK_TURN, CLIENT_COMMAND_FIND_OPPONENT, CLIENT_COMMAND_OPPONENT_RIGHT_TO_ATTACK, SERVER_COMMAND_ATTACK_BLOCK, SERVER_COMMAND_FOUND_OPPONENT, SERVER_COMMAND_LEFT_MATCH, SERVER_COMMAND_NOT_MATCHED, SERVER_COMMAND_OPPONENT_IS_ATTACKED_BLOCK, SERVER_COMMAND_OPPONENT_RIGHT_TO_ATTACK, SERVER_COMMAND_RIGHT_TO_ATTACK
from protocol.protocol_message import ProtocolMessage
from utils import recv_json, send_json

def handle_client(conn, addr, players, waiting_players):    
    try:
        print(f"[+] [NEW CONNECTION] {addr} connected.")
        players[conn] = { "address": addr, "opponent_addr": None, "inGame": False, "isMatching": False, "ships": [], "attackCoords": []}

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

                    attackedCoords = players[conn]["attackCoords"]
                    if [attack_x, attack_y] in attackedCoords:
                        send_json(conn, ProtocolMessage(SERVER_COMMAND_RIGHT_TO_ATTACK, {"right": True}))

                    opponent_addr = tuple(data.payload.get("opponent_addr"))

                    opponent_conn = None
                    for connection, info in players.items():
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
                        players[opponent_conn]["attackCoords"].append([attack_x, attack_y])
                    else:
                        print(f"Opponent address {opponent_addr} not found in players: {[info['address'] for info in players.values()]}")
                    send_json(conn, ProtocolMessage(SERVER_COMMAND_ATTACK_BLOCK, {"attack_y": attack_y, "attack_x": attack_x, "opponent_addr": opponent_addr}))
                    players[conn]["attackCoords"].append([attack_x, attack_y])
                elif command == CLIENT_COMMAND_OPPONENT_RIGHT_TO_ATTACK:
                    opponent_addr = tuple(data.payload.get("opponent_addr"))
                    opponent_conn = None
                    for connection, info in players.items():
                        if info["address"] == opponent_addr:
                            opponent_conn = connection
                            break

                    if opponent_conn:
                        send_json(opponent_conn, ProtocolMessage(SERVER_COMMAND_OPPONENT_RIGHT_TO_ATTACK,{ "right": False }))
                elif command == CLIENT_COMMAND__CANCEL_FIND_OPPONENT:
                    print("the waiting is ended")
                    if conn in waiting_players:
                        waiting_players.remove(conn)
                        print(f"[i] Removed {addr} from waiting_players.")
                else:
                    message = ProtocolMessage(SERVER_COMMAND_NOT_MATCHED, {"address": addr})
                    send_json(conn, message)
            except:
                print(f"[-] [ERROR] {addr}")
                break
    except Exception as e:
        print(f"[-] Exception for {addr}: {e}")

    finally:
        # Safely remove from waiting_players if present
        if conn in waiting_players:
            waiting_players.remove(conn)
            print(f"[i] Removed {addr} from waiting_players.")

        # Clean up from players dict
        if conn in players:
            opponent_addr = players[conn]["opponent_addr"]
            print("opponent_addr")
            opponent_conn = None
            for connection, info in players.items():
                if info["address"] == opponent_addr:
                    opponent_conn = connection
                    break

            if opponent_conn:
                # notify opponent connection
                message = ProtocolMessage(SERVER_COMMAND_LEFT_MATCH, {"address": addr})
                send_json(opponent_conn, message)
            del players[conn]
            print(f"[-] {addr} disconnected and removed from players.")

        print(f"[-] [DISCONNECT] {addr}")
        players.pop(conn, None)  # removes it if exists, does nothing otherwise (when the player disconnects)
        conn.close()
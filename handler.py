
from protocol.commands import SERVER_COMMAND_PING
from protocol.protocol_message import ProtocolMessage


def handle_client(conn, addr):    
    with conn:
        print(f"[+] [NEW CONNECTION] {addr} connected.")
        while True:
            try:
                # Decode the data with Protocol Message
                data = ProtocolMessage.decode(conn.recv(1024))
                if not data:
                    break
                print(f"[RECEIVED] {addr}: {data}")
                # Encode and send the data with Protocol Message
                message = ProtocolMessage(SERVER_COMMAND_PING)
                conn.sendall(message.encode()) 
            except:
                print(f"[-] [ERROR] {addr}")
                break
    
    print(f"[-] [DISCONNECT] {addr}")
    conn.close()

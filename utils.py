import struct
import json
from protocol.protocol_message import ProtocolMessage

def send_json(sock, data: ProtocolMessage):
    try:
        encoded_data = data.encode()
        length = struct.pack('>I', len(encoded_data))  # 4-byte big-endian length
        sock.sendall(length + encoded_data)
    except Exception as e:
        print(f"[SEND JSON ERROR] Failed to send data: {e}")

def recv_json(sock):
    try:
        raw_length = recvall(sock, 4)
        if not raw_length:
            return None

        message_length = struct.unpack('>I', raw_length)[0]
        message = recvall(sock, message_length)
        if not message:
            return None

        return ProtocolMessage.decode(message)

    except (ConnectionError, json.JSONDecodeError) as e:
        print(f"[RECEIVE JSON ERROR] {e}")
        return None
    except Exception as e:
        print(f"[RECEIVE JSON UNEXPECTED ERROR] {e}")
        return None

def recvall(sock, n):
    """Helper function to receive exactly n bytes or return None."""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

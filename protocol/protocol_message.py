import json
from typing import Optional

class ProtocolMessage:
    def __init__(self, command: str, payload: Optional[dict] = None):
        self.command = command
        self.payload = payload

    def encode(self) -> bytes:
        return json.dumps({
            "command": self.command,
            "payload": self.payload  # Can be None
        }).encode()

    @staticmethod
    def decode(data: bytes) -> "ProtocolMessage":
        obj = json.loads(data.decode())
        return ProtocolMessage(
            command=obj.get("command"),
            payload=obj.get("payload")  # Will be None if not present
        )
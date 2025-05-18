import json
from typing import Optional

from game import Ship

class ProtocolMessage:
    def __init__(self, command: str, payload: Optional[dict] = None):
        self.command = command
        self.payload = payload

    def encode(self) -> bytes:
        def serialize(obj):
            if isinstance(obj, Ship):
                return obj.to_dict()
            if isinstance(obj, (list, tuple)):
                return [serialize(item) for item in obj]
            if isinstance(obj, dict):
                return {key: serialize(value) for key, value in obj.items()}
            return obj  # fallback: return as-is (e.g., int, str)

        safe_payload = serialize(self.payload)
        return json.dumps({
            "command": self.command,
            "payload": safe_payload
        }).encode()

    @staticmethod
    def decode(data: bytes) -> "ProtocolMessage":
        obj = json.loads(data.decode())
        return ProtocolMessage(
            command=obj.get("command"),
            payload=obj.get("payload")  # Still a dict or None
        )

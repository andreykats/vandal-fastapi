from websocket import create_connection
from ..config import config
import json

BROADCAST_CHANNEL = "0"

def announce_reload():
    socket = create_connection(config.WEBSOCKET_URI)
    message = json.dumps({"action": "sendmessage", "payload": {"channel": BROADCAST_CHANNEL, "message": "reload"}})
    socket.send(message)
    socket.close()

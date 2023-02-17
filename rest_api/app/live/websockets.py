# from fastapi import WebSocket
from websocket import create_connection
from ..config import config
import json

BROADCAST_CHANNEL = "0"

# class WebsocketManager:
#     def __init__(self):
#         self.active_channels: dict[str, list[WebSocket]] = {}

#     async def connect(self, channel: str, websocket: WebSocket):
#         await websocket.accept()
#         # add websocket to array inside dictionary
#         if channel not in self.active_channels:
#             self.active_channels[channel] = []
#         self.active_channels[channel].append(websocket)

#     def disconnect(self, channel: str, websocket: WebSocket):
#         if channel in self.active_channels:
#             self.active_channels[channel].remove(websocket)

#     async def broadcast(self, channel: str, message: str):
#         for connection in self.active_channels[channel]:
#             await connection.send_text(message)


def announce_reload():
    socket = create_connection(config.WEBSOCKET_URI)
    message = json.dumps({"action": "sendmessage", "payload": {"channel": BROADCAST_CHANNEL, "message": "reload"}})
    socket.send(message)
    socket.close()

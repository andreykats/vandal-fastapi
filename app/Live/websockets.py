from fastapi import WebSocket
from typing import List
import json

from . import crud, schemas

BROADCAST_CHANNEL = 0


class WebsocketManager:
    def __init__(self):
        # self.active_connections: List[WebSocket] = []
        # dictionary of arrays of websockets
        self.active_channels: dict[int, List[WebSocket]] = {}

    # async def connect(self, websocket: WebSocket):
    #     await websocket.accept()
    #     self.active_connections.append(websocket)

    async def connect(self, channel: int, websocket: WebSocket):
        await websocket.accept()
        # add websocket to array inside dictionary
        if channel not in self.active_channels:
            self.active_channels[channel] = []
        self.active_channels[channel].append(websocket)

    # def disconnect(self, websocket: WebSocket):
    #     self.active_connections.remove(websocket)

    def disconnect(self, channel: int, websocket: WebSocket):
        if channel in self.active_channels:
            self.active_channels[channel].remove(websocket)

    # async def send(self, message: str, websocket: WebSocket):
    #     await websocket.send_text(json.dumps(message))

    # async def broadcast(self, message: str):
    #     for connection in self.active_connections:
    #         await connection.send_text(json.dumps(message))

    async def broadcast(self, channel: int, message: str):
        for connection in self.active_channels[channel]:
            await connection.send_text(message)


manager = WebsocketManager()


async def announce_new_message():
    message = json.dumps({"message": {"action": "reload"}})
    await manager.broadcast(BROADCAST_CHANNEL, message)

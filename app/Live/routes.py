from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import List
# import asyncio
import logging

# import aioredis
# from aioredis.client import Redis, PubSub

from ..utility import generate_unique_id


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/live",
    tags=["live"],
    generate_unique_id_function=generate_unique_id
)


@router.get("/{room}", response_class=HTMLResponse)
async def websocket_chat():
    return """
        <!DOCTYPE html>
        <html>

        <head>
            <title>Chat</title>
        </head>

        <body>
            <h1>WebSocket Chat</h1>
            <h2>Room: <span id="ws-id"></span></h2>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off" />
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
            <script>
                var client_id = 1
                const lastComponent = new URL(window.location).pathname.split("/").pop()
                document.querySelector("#ws-id").textContent = lastComponent;
                var ws = new WebSocket(`ws://localhost:8000/live/${lastComponent}`);
                ws.onmessage = function (event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                function sendMessage(event) {
                    var input = document.getElementById("messageText")
                    ws.send(input.value)
                    input.value = ''
                    event.preventDefault()
                }
            </script>
        </body>
        </html>
        """


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


@router.websocket("/")
# Broadcast message to all websocket connections
async def websocket_broadcast(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # print(f"Received message from {websocket}: {data}")
            await manager.broadcast(data)
            # await manager.send({"item_id": item_id, "message": data}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: int):
    await manager.connect(channel, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # print(f"Received message from {channel}: {data}")
            await manager.broadcast(channel, data)
            # await manager.send({"item_id": item_id, "message": data}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(channel, websocket)

######################


# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     await redis_connector(websocket)


# async def redis_connector(websocket: WebSocket):
#     async def consumer_handler(conn: Redis, ws: WebSocket):
#         try:
#             while True:
#                 message = await ws.receive_text()
#                 if message:
#                     await conn.publish("chat:c", message)
#         except WebSocketDisconnect as exc:
#             # TODO this needs handling better
#             logger.error(exc)

#     async def producer_handler(pubsub: PubSub, ws: WebSocket):
#         await pubsub.subscribe("chat:c")
#         # assert isinstance(channel, PubSub)
#         try:
#             while True:
#                 message = await pubsub.get_message(ignore_subscribe_messages=True)
#                 if message:
#                     await ws.send_text(message.get('data'))
#         except Exception as exc:
#             # TODO this needs handling better
#             logger.error(exc)

#     conn = await get_redis_pool()
#     pubsub = conn.pubsub()

#     consumer_task = consumer_handler(conn=conn, ws=websocket)
#     producer_task = producer_handler(pubsub=pubsub, ws=websocket)
#     done, pending = await asyncio.wait(
#         [consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED,
#     )
#     logger.debug(f"Done task: {done}")
#     for task in pending:
#         logger.debug(f"Canceling task: {task}")
#         task.cancel()


# async def get_redis_pool():
#     return await aioredis.from_url(f'redis://localhost', encoding="utf-8", decode_responses=True)

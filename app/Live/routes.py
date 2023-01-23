from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
# from typing import List
import logging

from . import crud, schemas
from ..utility import generate_unique_id
from ..dependencies import get_ddb
from .websockets import manager

from boto3.resources.base import ServiceResource


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BROADCAST_CHANNEL = 0


router = APIRouter(
    prefix="/live",
    tags=["live"],
    generate_unique_id_function=generate_unique_id
)


@router.websocket("/")
# Broadcast message to all websocket connections
async def websocket_broadcast(websocket: WebSocket):
    await manager.connect(BROADCAST_CHANNEL, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # print(f"Received message from {websocket}: {data}")
            await manager.broadcast(BROADCAST_CHANNEL, data)
            # await manager.send({"item_id": item_id, "message": data}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(BROADCAST_CHANNEL, websocket)


@router.websocket("/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: int):
    await manager.connect(channel, websocket)

    # When sockets connect, send them the current list of messages
    message_list = crud.get_messages(channel)
    for message in message_list:
        await websocket.send_text(message["body"])
        print(message["body"])
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(channel, data)

            # Create a new message in the database
            msg = schemas.MessageCreate(channel=channel, body=data)
            crud.create_message(msg)

    except WebSocketDisconnect:
        manager.disconnect(channel, websocket)


@router.get("/")
def dyanamodb_admin():
    return RedirectResponse("http://localhost:8001")


@router.post("/", response_model=list[schemas.Layer])
def create_messages(items: list[schemas.MessageCreate]):
    message_list = []
    for x in items:
        message = crud.create_message(message=x)
        message_list.append(message)

    return message_list


@router.get("/{channel}", response_model=list[schemas.Layer])
def get_messages(channel: str):
    message_list = crud.get_messages(channel)
    return message_list


@router.delete("/{channel}")
def delete_channel_content(channel: str):
    result = crud.delete_messages(channel=channel)
    return result


@router.get("/chat/{channel}", response_class=HTMLResponse)
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
                var ws = new WebSocket(`ws://localhost:8080/live/${lastComponent}`);
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

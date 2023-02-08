from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
from typing import Iterator, AsyncIterator

from . import schemas, crud
from ..config import config
from ..utility import generate_unique_id

# from ..dependencies import get_ddb
# from .websockets import manager, BROADCAST_CHANNEL
# from boto3.resources.base import ServiceResource

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/websockets",
    tags=["websockets"],
    generate_unique_id_function=generate_unique_id
)


@router.post("/create", response_model=list[schemas.Message])
async def create_messages(body: list[schemas.MessageCreate]):
    try:
        message_list = []
        for message in body:
            model = await crud.create_message(message=message)
            message_list.append(schemas.Message(**model.attribute_values))
        return message_list
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.get("/get/{channel}", response_model=list[schemas.Message])
async def get_messages(channel: str):
    try:
        message_list = await crud.get_messages(channel)
        return message_list
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.delete("/delete/{channel}")
async def delete_channel_content(channel: str):
    try:
        result = await crud.delete_channel_history(channel=channel)
        return result
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.get("/chat/{channel}", response_class=HTMLResponse)
async def websocket_chat(channel: str):
    return f"""
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
                var ws = new WebSocket(`{config.WEBSOCKET_URI}?channel={channel}');
                ws.onmessage = function (event) {{
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                }};
                function sendMessage(event) {{
                    var input = document.getElementById("messageText")
                    ws.send(input.value)
                    input.value = '{{"action": "sendmessage", "payload": {"channel": "1", "message": "hello"}}}'
                    event.preventDefault()
                }}
            </script>
        </body>
        </html>
        """

        
# MESSAGE_STREAM_DELAY = 1  # second
# MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # milisecond

# COUNTER = 0
# def get_message_for_channel():
#     global COUNTER
#     COUNTER += 1
#     return COUNTER, COUNTER < 1000

# async def event_generator(request: Request) -> AsyncIterator[str]:
#     while True:
#         if await request.is_disconnected():
#             print("Request disconnected")
#             break

#         # Checks for new messages and return them to client if any
#         counter, exists = get_message_for_channel()
#         if exists:
#             yield json.dumps({
#                 "event": "new_message",
#                 "id": "message_id",
#                 "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
#                 "data": f"Counter value {counter}",
#             })
#         else:
#             yield json.dumps({
#                 "event": "end_event",
#                 "id": "message_id",
#                 "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
#                 "data": "End of the stream",
#             })
#         await asyncio.sleep(MESSAGE_STREAM_DELAY)

# @router.get("/stream")
# async def message_stream(request: Request):
#     response = StreamingResponse(event_generator(request), media_type="text/event-stream")
#     response.headers["Cache-Control"] = "no-cache"
#     response.headers["X-Accel-Buffering"] = "no"
#     return response

# @router.post("/stream", response_model=list[schemas.Message])
# async def create_messages_test(body: list[schemas.MessageCreate]):
#     try:
#         message_list = []
#         for message in body:
#             model = await crud.create_message(message=message)
#             message_list.append(schemas.Message(**model.attribute_values))

#         return message_list
#     except Exception as error:
#         raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})

# @router.websocket("/")
# # Broadcast message to all websocket connections
# async def websocket_broadcast(websocket: WebSocket):
#     await manager.connect(BROADCAST_CHANNEL, websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # print(f"Received message from {websocket}: {data}")
#             await manager.broadcast(BROADCAST_CHANNEL, data)
#             # await manager.send({"item_id": item_id, "message": data}, websocket)
#     except WebSocketDisconnect:
#         manager.disconnect(BROADCAST_CHANNEL, websocket)


# @router.websocket("/{channel}")
# async def websocket_endpoint(websocket: WebSocket, channel: str):
#     await manager.connect(channel=channel, websocket=websocket)

#     # When sockets connect, send them the current list of messages
#     message_list = await crud.get_messages(channel=channel)
#     for message in message_list:
#         await websocket.send_text(message.body)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast(channel, data)

#             # Create a new message in the database
#             await crud.create_message(message=schemas.MessageCreate(channel=channel, body=data))

#     except WebSocketDisconnect:
#         manager.disconnect(channel, websocket)


# @router.get("/")
# def dyanamodb_admin():
#     return RedirectResponse("http://localhost:8001")
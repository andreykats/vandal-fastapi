from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import List
import asyncio
import random

from ..utility import generate_unique_id


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    generate_unique_id_function=generate_unique_id
)


@router.get("/")
async def redirect():
    # Redirect to the docs route for now
    return RedirectResponse("/docs")

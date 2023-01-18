from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import List
import logging

from . import crud, schemas
from ..utility import generate_unique_id
from ..dependencies import get_ddb

from boto3.resources.base import ServiceResource


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/art-dynamodb",
    tags=["art-dynamodb"],
    generate_unique_id_function=generate_unique_id
)


@router.get("/", response_model=list[schemas.Layer])
def get_all_items(rate_limit: int = 15):
    items = crud.get_all_items(rate_limit=rate_limit)
    print(items)
    return items


@router.post("/", response_model=list[schemas.Layer])
def create_items(items: list[schemas.LayerCreate]):
    item_list = []
    for x in items:
        item = crud.create_item(item=x)
        item_list.append(item)

    return item_list

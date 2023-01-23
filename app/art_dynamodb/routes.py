from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import List
import logging

from . import crud, schemas
from ..utility import generate_unique_id
from ..dependencies import get_ddb

from boto3.resources.base import ServiceResource

import os
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/art-dynamodb",
    tags=["art-dynamodb"],
    generate_unique_id_function=generate_unique_id
)


@router.post("/", response_model=list[schemas.Layer])
async def create_layers(body: list[schemas.LayerCreate]):
    try:
        layer_list = []
        for layer in body:
            layer_list.append(await crud.create_layer(schema=layer))
        return layer_list
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.post("/activate", response_model=schemas.Layer)
async def set_artwork_active(layer_id: str, is_active: bool):
    try:
        return await crud.set_artwork_active(layer_id=layer_id, is_active=is_active)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.get("/base", response_model=list[schemas.Layer])
async def get_all_base_layers(rate_limit: int = 15):
    try:
        return await crud.get_all_base_layers(rate_limit=rate_limit)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.get("/created", response_model=list[schemas.Layer])
async def get_all_created_layers(rate_limit: int = 15):
    try:
        return await crud.get_all_created_layers(rate_limit=rate_limit)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.get("/latest", response_model=list[schemas.Artwork])
def get_latest_artworks():
    return crud.get_latest_artworks()


@router.get("/{layer_id}", response_model=schemas.Artwork)
async def get_artwork(layer_id: str):
    artwork = await crud.get_artwork(layer_id=layer_id)
    if artwork is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return artwork


@router.delete("/{layer_id}", response_model=schemas.Layer)
async def delete_created_content(layer_id: str, created_at: datetime.datetime):
    layer = await crud.delete_created_layer(layer_id=layer_id, created_at=created_at)

    # Delete stored image file
    try:
        os.remove("./images/" + layer.file_name)
    except:
        pass

    if layer is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return layer


@router.get("/{layer_id}/history", response_model=list[schemas.Artwork])
async def get_artwork(layer_id: str):
    history = await crud.get_artwork_history(layer_id=layer_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return history

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from pynamodb.exceptions import DoesNotExist, DeleteError, GetError, ScanError, QueryError, TableError, TableDoesNotExist

from . import crud_ddb as crud, files, schemas
from ..utility import generate_unique_id
from ..live import crud as live_crud, websockets
from .. import auth
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/art",
    tags=["art"],
    generate_unique_id_function=generate_unique_id
)


@router.post("/create", dependencies=[Depends(auth.admin)])
async def create_layers(body: list[schemas.LayerCreate]) -> list[schemas.Layer]:
    try:
        layer_list = []
        for layer in body:
            model = await crud.create_layer(layer)
            layer_list.append(schemas.Layer(**model.attribute_values))
        return layer_list
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.post("/submit", dependencies=[Depends(auth.user)])
async def submit_new_layer(
    layer_id: str = Form(...), 
    user_id: str = Form(...), 
    image_data: str = Form(...)) -> schemas.Artwork:

    try:
        model = await crud.set_layer_active(layer_id=layer_id, is_active=False)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})

    try:
        new_layer = await crud.create_layer(schemas.LayerCreate(owner_id=user_id, base_layer_id=model.base_layer_id, width=model.width, height=model.height, art_name=model.art_name, artist_name=model.artist_name))
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error), "X-Error-Name": "create_layer"})

    try:
        file_name = (new_layer.id + ".jpg").replace(" ", "_")
        print(file_name)
        await files.save_image_data_to_s3(file_name=file_name, image_data=image_data)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error), "X-Error-Name": "save_image_data"})

    try:
        artwork = await crud.get_artwork_from_layer(layer=new_layer)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error))

    try:
        websockets.announce_reload()
    except Exception as error:
        pass

    return artwork


@router.post("/upload", dependencies=[Depends(auth.admin)])
async def upload_base_layer(
    art_name: str = Form(...), 
    artist_name: str = Form(...), 
    user_id: str = Form(...), 
    image_width: int = Form(...), 
    image_height: int = Form(...), 
    image_file: UploadFile = File(...)) -> schemas.Layer:

    try:
        new_layer = await crud.create_layer(schemas.LayerCreate(owner_id=user_id, art_name=art_name, artist_name=artist_name, width=image_width, height=image_height))
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})

    try:
        file_name = (new_layer.id + ".jpg").replace(" ", "_")
        await files.save_image_file_to_s3(file_name=file_name, image_file=image_file.file)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})

    try:
        websockets.announce_reload()
    except Exception as error:
        pass

    return schemas.Layer(**new_layer.attribute_values)


@router.post("/activate", dependencies=[Depends(auth.admin)])
async def set_artwork_active(
    layer_id: str = Form(...), 
    is_active: bool = Form(...)) -> schemas.Artwork:

    try:
        model = await crud.set_layer_active(layer_id=layer_id, is_active=is_active)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})

    try:
        artwork = await crud.get_artwork_from_layer(layer=model)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})

    if artwork.is_active == False:
        try:
            # Delete all messages from DynamoDB if artwork is being deactivated
            await live_crud.delete_channel_history(artwork.id)
        except Exception as error:
            raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})

    try:
        websockets.announce_reload()
    except Exception as error:
        pass

    return artwork


@router.get("/base")
async def get_all_base_layers(rate_limit: int = 15) -> list[schemas.Layer]:
    try:
        return await crud.get_all_base_layers(rate_limit=rate_limit)
    except ScanError as error:
        raise HTTPException(status_code=404, detail=str(error), headers={"X-Error": str(error)})
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.get("/created")
async def get_all_created_layers(rate_limit: int = 15) -> list[schemas.Layer]:
    try:
        return await crud.get_all_created_layers(rate_limit=rate_limit)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.get("/latest")
async def get_latest_artworks() -> list[schemas.Artwork]:
    try:
        return await crud.get_latest_artworks()
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.get("/get/{layer_id}")
async def get_artwork(layer_id: str) -> schemas.Artwork:
    try:
        return await crud.get_artwork_from_id(layer_id=layer_id)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.get("/history/{layer_id}")
async def get_artwork_history(layer_id: str) -> list[schemas.Artwork]:
    try:
        return await crud.get_artwork_history(layer_id=layer_id)
    except QueryError as error:
        raise HTTPException(status_code=404, detail=str(error), headers={"X-Error": str(error)})
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})


@router.delete("/delete/{layer_id}", dependencies=[Depends(auth.admin)])
async def delete_created_content(layer_id: str) -> schemas.Layer:
    try:
        layer = await crud.delete_layer(layer_id=layer_id)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})

    try:
        # Delete stored image file
        if layer.file_name:
            await files.delete_file_from_disk(file_name=layer.file_name)
        else:
            file_name = (layer.id + ".jpg").replace(" ", "_")
            await files.delete_file_from_disk(file_name=file_name)
    except Exception as error:
        raise HTTPException(status_code=503, detail=str(error), headers={"X-Error": str(error)})

    try:
        websockets.announce_reload()
    except Exception as error:
        pass

    return layer

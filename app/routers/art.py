from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import crud, schemas
import base64
import uuid
import shutil

from PIL import Image
import io


router = APIRouter(
    prefix="/art",
    tags=["art"]
)


@router.get("/", response_model=list[schemas.Item])
def get_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_all_items(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_single_item(db, item_id=item_id)
    return item


@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = crud.create_item(db=db, item=item)
    return item


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.delete_item(db=db, item_id=item_id)
    return item


@router.get("/row/", response_model=list[schemas.Item])
def get_all_row_items(db: Session = Depends(get_db)):
    items = crud.get_feed_items(db)
    return items


@router.get("/row/{item_id}", response_model=list[schemas.Item])
def get_row_items(item_id: int, db: Session = Depends(get_db)):
    items = crud.get_row_items(db, item_id=item_id)
    return items


# @router.post("/upload")
# def upload(item: schemas.ItemCreate = Form(...), filedata: str = Form(...), db: Session = Depends(get_db)):
#     # Convert string to bytes
#     image_as_bytes = str.encode(filedata)

#     # Decode base64string back to image
#     img = base64.b64decode(image_as_bytes)

#     filename = str(uuid.uuid4()) + ".png"

#     # Create file and write bits
#     with open("./images/" + filename, "wb") as f:
#         f.write(img)

#     item = crud.create_item(db=db, item=item, url=filename)
#     return item


@router.post("/upload")
def upload_image_layer(filedata: str = Form(...), filename: str = Form(...), parentname: str = Form(...)):
    # Convert string to bytes
    image_as_bytes = str.encode(filedata)

    # Decode base64string back to image
    img = base64.b64decode(image_as_bytes)

    # Read background image from file into PIL
    background = Image.open("./images/" + parentname + ".jpg")

    # Read overlay image from byte string into PIL
    overlay = Image.open(io.BytesIO(img))

    '''
    First parameter to .paste() is the image to paste. Second are coordinates, and the secret sauce is the third parameter. It indicates a mask that will be used to paste the image. If you pass a image with transparency, then the alpha channel is used as mask.
    '''
    background.paste(overlay, (0, 0), overlay)

    # Save to file with provited filename
    background.save("./images/" + filename, "PNG")

    return {"filename": filename}

    # filename = str(uuid.uuid4()) + ".jpg"
    # Create file and write bits
    # with open("./images/" + filename, "wb") as f:
    #     f.write(img)
    #     return {"filename": filename}


# @router.post("/uploadfile/", response_model=schemas.Item)
# async def create_upload_file(image: UploadFile = File(...), item: schemas.ItemCreate, db: Session = Depends(get_db)):
#     print({"filename": image.filename})
#     item = crud.create_item(db=db, item=item)

#     # filename = item.id + ".jpg"
#     # # Create file and write bits
#     # with open("./images/" + filename, "wb") as buffer:
#     #     # f.write(file.file.read())
#     #     shutil.copyfileobj(image.file, buffer)

#     return item

@router.post("/bulk", response_model=list[schemas.Item])
def create_bulk_items(items: list[schemas.ItemCreate], db: Session = Depends(get_db)):
    item_list = []
    for x in items:
        item = crud.create_item(db=db, item=x)
        item_list.append(item)
    return item_list

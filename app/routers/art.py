from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import crud, schemas
import base64
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


@router.post("/", response_model=list[schemas.Item])
def create_items(items: list[schemas.ItemCreate], db: Session = Depends(get_db)):
    item_list = []
    for x in items:
        item = crud.create_item(db=db, item=x)
        item_list.append(item)

    return item_list


@router.get("/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)
    return item


'''
@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = crud.create_item(db=db, item=item)
    return item
'''

'''
@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.delete_item(db=db, item_id=item_id)
    return item
'''


@router.post("/submit", response_model=schemas.Item)
def create_modified_item(item_id: int = Form(...), user_id: int = Form(...), image_data: str = Form(...), db: Session = Depends(get_db)):
    parent_item = crud.get_item(db, item_id=item_id)

    child_item = schemas.ItemCreate(name=parent_item.name, owner_id=user_id, base_layer_id=parent_item.base_layer_id)
    child_item = crud.create_item(db=db, item=child_item)

    # Convert string to bytes
    image_as_bytes = str.encode(image_data)

    # Decode base64string back to image
    img = base64.b64decode(image_as_bytes)
    file_name = str(child_item.id) + ".jpg"

    # If the image from parent item is actially the base art image then skip the blending step and just save it to file.
    if parent_item.id == parent_item.base_layer_id:
        with open("./images/" + file_name, "wb") as buffer:
            buffer.write(img)
            return child_item

    # Read background image from file into PIL
    background = Image.open("./images/" + str(parent_item.id) + ".jpg")

    # Read overlay image from byte string into PIL
    overlay = Image.open(io.BytesIO(img))

    # First parameter to .paste() is the image to paste.
    # Second are coordinates, and the secret sauce is the third parameter.
    # It indicates a mask that will be used to paste the image.
    # If you pass a image with transparency, then the alpha channel is used as mask.
    background.paste(overlay, (0, 0), overlay)

    # Save to file with provited filename
    background.save("./images/" + file_name, "PNG")

    return child_item


@router.get("/feed/", response_model=list[schemas.Item])
def get_new_feed_items(db: Session = Depends(get_db)):
    items = crud.get_feed_items(db)
    return items


@router.get("/feed/{item_id}", response_model=list[schemas.Item])
def get_item_history(item_id: int, db: Session = Depends(get_db)):
    items = crud.get_row_items(db, item_id=item_id)
    return items


'''
# BROKE DUE TO COMMENTED OUT VALIDATION FUNCTIONS IN MODEL
@router.post("/upload/json", response_model=schemas.Item)
async def upload_art_with_json(item: schemas.ItemCreate, image: UploadFile = File(...), db: Session = Depends(get_db)):
    print({"filename": image.filename})
    item = crud.create_item(db=db, item=item)

    filename = str(item.id) + ".jpg"
    with open("./images/" + filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return item
'''


@router.post("/upload", response_model=schemas.Item)
async def create_and_upload_a_new_item(name: str = Form(...), user_id: int = Form(...), image: UploadFile = File(...), db: Session = Depends(get_db)):
    print({"filename": image.filename})
    item = schemas.ItemCreate(name=name, owner_id=user_id)
    item = crud.create_item(db=db, item=item)

    filename = str(item.id) + ".jpg"
    with open("./images/" + filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return item

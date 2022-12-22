from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import crud, schemas
import base64


router = APIRouter(
    prefix="/art",
    tags=["art"]
)


@router.get("/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = crud.create_item(db=db, item=item)
    return item


@router.post("/upload")
def upload(filename: str = Form(...), filedata: str = Form(...)):
    # Convert string to bytes
    image_as_bytes = str.encode(filedata)

    # Decode base64string back to image
    img = base64.b64decode(image_as_bytes)

    # Create file and write bits
    with open("./images/" + filename, "wb") as f:
        f.write(img)
    return {"message": f"Successfuly uploaded {filename}"}

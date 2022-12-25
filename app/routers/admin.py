from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import crud
import os

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.delete("/{item_id}")
def delete_user_content(item_id: int, db: Session = Depends(get_db)):
    item = crud.delete_user_item(db=db, item_id=item_id)

    # Delete stored image file
    os.remove("./images/" + str(item.id) + ".jpg")

    return item


@router.post("/destroy/")
def delete_all_user_created_content(db: Session = Depends(get_db)):
    items = crud.delete_all_user_items(db=db)

    count = 0
    for item in items:
        # Delete stored image file
        os.remove("./images/" + str(item.id) + ".jpg")
        count += 1

    return {"deleted": count}

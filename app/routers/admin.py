from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import crud


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.delete("/{item_id}")
def delete_content(item_id: int, db: Session = Depends(get_db)):
    response = crud.delete_user_content(db=db, item_id=item_id)
    return response


@router.post("/destroy/")
def delete_all_user_created_content(db: Session = Depends(get_db)):
    response = crud.delete_all_user_content(db=db)
    return response

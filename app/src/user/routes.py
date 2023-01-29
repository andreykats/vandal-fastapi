# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.routing import APIRoute
# from sqlalchemy.orm import Session

# from ..dependencies import get_db
# from . import crud, schemas
# from ..utility import generate_unique_id


# router = APIRouter(
#     prefix="/users",
#     tags=["users"],
#     generate_unique_id_function=generate_unique_id
# )


# @router.post("/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @router.get("/", response_model=list[schemas.User])
# def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @router.get("/{user_id}", response_model=schemas.User)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

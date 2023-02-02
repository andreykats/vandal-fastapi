# from fastapi import APIRouter, Depends, Form, File, UploadFile
# from sqlalchemy.orm import Session
# import base64
# import shutil
# import os
# # import io
# # from PIL import Image

# from ..dependencies import get_db
# from . import crud, schemas
# from ..utility import generate_unique_id
# from ..live import websockets


# router = APIRouter(
#     prefix="/art",
#     tags=["art"],
#     generate_unique_id_function=generate_unique_id
# )


# @router.get("/", response_model=list[schemas.Item])
# def get_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_all_items(db, skip=skip, limit=limit)
#     return items


# @router.post("/", response_model=list[schemas.Item])
# def create_items(items: list[schemas.ItemCreate], db: Session = Depends(get_db)):
#     item_list = []
#     for x in items:
#         item = crud.create_item(db=db, item=x)
#         item_list.append(item)

#     return item_list


# @router.get("/{item_id}", response_model=schemas.Artwork)
# def get_artwork(item_id: int, db: Session = Depends(get_db)):
#     return crud.get_artwork(db, item_id=item_id)


# '''
# @router.post("/", response_model=schemas.Item)
# def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
#     item = crud.create_item(db=db, item=item)
#     return item
# '''

# '''
# @router.delete("/{item_id}")
# def delete_item(item_id: int, db: Session = Depends(get_db)):
#     item = crud.delete_item(db=db, item_id=item_id)
#     return item
# '''


# @router.post("/upload", response_model=schemas.Item)
# async def create_base_item(name: str = Form(...), user_id: int = Form(...), image: UploadFile = File(...), db: Session = Depends(get_db)):
#     print({"filename": image.filename})
#     db_item = schemas.ItemCreate(name=name, owner_id=user_id)
#     item = crud.create_item(db=db, item=db_item)

#     filename = str(item.id) + ".jpg"
#     with open("./images/" + filename, "wb") as buffer:
#         shutil.copyfileobj(image.file, buffer)

#     return item


# @router.post("/submit", response_model=schemas.Artwork)
# async def create_vandalized_item(item_id: int = Form(...), user_id: int = Form(...), image_data: str = Form(...), db: Session = Depends(get_db)):

#     # Set incoming layer back to inactive
#     parent_item = await crud.set_item_active(db, item_id=item_id, is_active=False)

#     # Create new layer
#     db_item = schemas.ItemCreate(name=parent_item.name, owner_id=user_id, base_layer_id=parent_item.base_layer_id, height=parent_item.height, width=parent_item.width)
#     item = crud.create_item(db=db, item=db_item)

#     # Convert string to bytes
#     image_as_bytes = str.encode(image_data)

#     # Decode base64string back to image
#     img = base64.b64decode(image_as_bytes)
#     file_name = str(item.id) + ".jpg"

#     # Save image to disk
#     with open("./images/" + file_name, "wb") as buffer:
#         buffer.write(img)

#     # Broadcast notifiction over websocket
#     await websockets.announce_reload()

#     return crud.get_artwork(db, item.id)


# @router.post("/activate", response_model=schemas.Artwork)
# async def set_artwork_active(item_id: int = Form(...), is_active: bool = Form(...), db: Session = Depends(get_db)):
#     item = await crud.set_item_active(db, item_id=item_id, is_active=is_active)

#     # Broadcast notifiction over websocket
#     await websockets.announce_reload()

#     return crud.get_artwork(db, item_id=item.id)


# @router.get("/feed/", response_model=list[schemas.Artwork])
# def get_feed_items(db: Session = Depends(get_db)):
#     return crud.get_feed_items(db)


# @router.get("/history/{item_id}", response_model=list[schemas.Artwork])
# def get_artwork_history(item_id: int, db: Session = Depends(get_db)):
#     return crud.get_artwork_history(db, item_id=item_id)


# '''
# # BROKE DUE TO COMMENTED OUT VALIDATION FUNCTIONS IN MODEL
# @router.post("/upload/json", response_model=schemas.Item)
# async def upload_art_with_json(item: schemas.ItemCreate, image: UploadFile = File(...), db: Session = Depends(get_db)):
#     print({"filename": image.filename})
#     item = crud.create_item(db=db, item=item)

#     filename = str(item.id) + ".jpg"
#     with open("./images/" + filename, "wb") as buffer:
#         shutil.copyfileobj(image.file, buffer)

#     return item
# '''


# @router.delete("/{item_id}")
# def delete_user_content(item_id: int, db: Session = Depends(get_db)):
#     item = crud.delete_user_item(db=db, item_id=item_id)

#     # Delete stored image file
#     try:
#         os.remove("./images/" + str(item.id) + ".jpg")
#     except:
#         pass

#     return item


# @router.post("/destroy/")
# def delete_all_user_created_content(db: Session = Depends(get_db)):
#     items = crud.delete_all_user_items(db=db)

#     count = 0
#     for item in items:
#         # Delete stored image file
#         os.remove("./images/" + str(item.id) + ".jpg")
#         count += 1

#     return {"deleted": count}

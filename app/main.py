from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .database import engine
from . import models
from .routers import art, users

models.Base.metadata.create_all(bind=engine)

api = FastAPI()

api.include_router(users.router)
api.include_router(art.router)


@api.get("/")
async def redirect():
    return RedirectResponse("/docs")

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .database import engine
from . import models
from .routers import art, users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

models.Base.metadata.create_all(bind=engine)

description = """
FastAPI based backend providing a REST API 🚀

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).

## Items

You can **read items**.

"""

api = FastAPI(
    title="Vandal REST API",
    description=description,
    version="0.0.1"
)
origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(users.router)
api.include_router(art.router)
api.mount("/images", StaticFiles(directory="images"), name="images")


@api.get("/")
async def redirect():
    return RedirectResponse("/docs")

if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)

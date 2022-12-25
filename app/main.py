from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import admin, art, users


description = """
### FastAPI based backend providing a REST API 🚀

Authentication not yet implemented
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


api.include_router(art.router)
api.include_router(users.router)
api.include_router(admin.router)


api.mount("/images", StaticFiles(directory="images/"), name="images")
api.mount("/", StaticFiles(directory="build/", html=True), name="build")

# @api.get("/")
# async def redirect():
#     return RedirectResponse("/docs")

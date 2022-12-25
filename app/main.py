from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import admin, art, users
from typing import Callable

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


def update_schema_name(app: FastAPI, function: Callable, name: str) -> None:
    """
    Updates the Pydantic schema name for a FastAPI function that takes
    in a fastapi.UploadFile = File(...) or bytes = File(...).

    This is a known issue that was reported on FastAPI#1442 in which
    the schema for file upload routes were auto-generated with no
    customization options. This renames the auto-generated schema to
    something more useful and clear.

    Args:
        app: The FastAPI application to modify.
        function: The function object to modify.
        name: The new name of the schema.
    """
    for route in app.routes:
        print(route)
        if route.endpoint is function:
            route.body_field.type_.__name__ = name
            break


update_schema_name(api, art.create_modified_item, "Submit")
update_schema_name(api, art.create_and_upload_a_new_item, "Upload")

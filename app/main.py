from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from typing import Callable

from .database import Base, engine
from .UserService import routes as users
from .ArtService import routes as art

description = """
### FastAPI based backend providing a REST API 🚀

### To Do:
* **Set up JWT based authentication**.
* **Switch database from SQLite to PostgreSQL**.
"""


api = FastAPI(
    title="Vandal REST API",
    description=description,
    version="0.0.2"
)
origins = ['http://localhost:3000']

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api.include_router(art.router)
api.include_router(users.router)


api.mount("/images", StaticFiles(directory="images/"), name="images")
# api.mount("/", StaticFiles(directory="build/", html=True), name="build")


@api.get("/")
async def redirect():
    return RedirectResponse("/docs")


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


update_schema_name(api, art.create_vandalized_item, "FormVandalizedItem")
update_schema_name(api, art.create_base_item, "FormBaseItem")


# Run database migration
Base.metadata.create_all(bind=engine)

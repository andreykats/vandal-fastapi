from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from .database import Base, engine
from .UserService import routes as users
from .ArtService import routes as art
from .AdminService import routes as admin
from .utility import update_schema_name

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
api.include_router(admin.router)


update_schema_name(api, art.create_vandalized_item, "FormVandalizedItem")
update_schema_name(api, art.create_base_item, "FormBaseItem")


api.mount("/images", StaticFiles(directory="images/"), name="images")
# api.mount("/", StaticFiles(directory="build/", html=True), name="build")


@api.get("/")
async def redirect():
    return RedirectResponse("/docs")


# Run database migration
Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from .database import Base, engine
from .utility import update_schema_name
from .User import routes as users
from .Art import routes as art
from .Admin import routes as admin
from .Live import routes as live


description = """
### FastAPI based backend providing a REST API 🚀

### To Do:
* **Set up JWT based authentication**.
* **Switch database from SQLite to PostgreSQL**.
"""

# Create a FastAPI instance
api = FastAPI(
    title="Vandal REST API",
    description=description,
    version="0.0.2"
)

# Add CORS handling. For dev everything is set to open
api.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add the individual service routers to the main api process
api.include_router(art.router)
api.include_router(users.router)
api.include_router(admin.router)


# Manually set non-pydantic schema names
update_schema_name(api, art.create_vandalized_item, "FormVandalizedItem")
update_schema_name(api, art.create_base_item, "FormBaseItem")


# Add mounted directories serving static files
api.mount("/images", StaticFiles(directory="images/"), name="images")
# api.mount("/", StaticFiles(directory="build/", html=True), name="build")


# Run database migration
Base.metadata.create_all(bind=engine)


# Specify the root route
@api.get("/")
async def redirect():
    # Redirect to the docs route for now
    return RedirectResponse("/docs")

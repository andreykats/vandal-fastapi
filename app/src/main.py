from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# from .db_sql import Base, engine
from .utility import update_schema_name, logger
# from .user import routes as users
from .admin import routes as admin
from .live import routes as live
from .art import routes as art

from mangum import Mangum
from dotenv import load_dotenv
from os import environ

load_dotenv()

description = """
### FastAPI based backend providing a REST API 🚀

### To Do:
* **Set up JWT based authentication**.
* **Switch database from SQLite to PostgreSQL**.
"""

root_path = "/" + environ.get('VANDAL_ENV', "")

print(f"Setting root_path to:  {root_path}")
logger.debug(f"Setting root_path to: {root_path}")

# Create a FastAPI instance
api = FastAPI(
    title="Vandal REST API",
    description=description,
    version="0.0.2",
    openapi_url="/openapi.json",
    root_path= root_path,
)

# Add CORS handling. For dev everything is set to open
api.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add the individual service routers to the main api process
api.include_router(art.router)
# api.include_router(users.router)
api.include_router(admin.router)
api.include_router(live.router)

# Manually set non-pydantic schema names
update_schema_name(api.routes, art.submit_new_layer, "FormNewLayer")
update_schema_name(api.routes, art.upload_base_layer, "FormBaseLayer")
update_schema_name(api.routes, art.set_artwork_active, "FormActivate")

# Add mounted directories serving static files
# api.mount("/images", StaticFiles(directory="images/"), name="images")
# api.mount("/", StaticFiles(directory="build/", html=True), name="build")


# Run database migration
# Base.metadata.create_all(bind=engine)


# Specify the root route
@api.get("/")
async def redirect():
    # Redirect to the docs route for now
    return RedirectResponse("/docs")

# Add a sanity check route
@api.get("/ping")
def pong():
    return "pong"

# Wrap the FastAPI instance for AWS Lambda
handler = Mangum(api)

# Add logging
handler = logger.inject_lambda_context(handler, clear_state=True)
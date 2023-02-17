from fastapi import FastAPI, __version__ as fastapi_version, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from .utility import update_schema_name, logger
from .user import routes as users
from .admin import routes as admin
from .live import routes as live
from .art import routes as art

from mangum import Mangum
from dotenv import load_dotenv
from os import environ


load_dotenv()
# Set the root path for the environment
if "dev" in environ.get('ENV', "").lower():
    root_path = "/"
elif "stage" in environ.get('ENV', "").lower():
    root_path = "/Stage"
elif "prod" in environ.get('ENV', "").lower():
    root_path = "/Prod"
else:
    raise ValueError("ENV not set")

# print(f"Setting root_path to:  {root_path}")
# logger.debug(f"Setting root_path to: {root_path}")

# Create a FastAPI instance
title = "VANDAL REST API"
description = f"""
### FastAPI based backend providing a REST API 🚀
"""
api = FastAPI(
    title=title,
    description=description,
    version=fastapi_version,
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
api.include_router(users.router)
api.include_router(live.router)
api.include_router(admin.router)

# Manually set non-pydantic schema names
update_schema_name(api.routes, art.submit_new_layer, "FormNewLayer")
update_schema_name(api.routes, art.upload_base_layer, "FormBaseLayer")
update_schema_name(api.routes, art.set_artwork_active, "FormActivate")
update_schema_name(api.routes, users.login, "FormLogin")
update_schema_name(api.routes, users.signup, "FormSignup")

# Add mounted directories serving static files
# api.mount("/images", StaticFiles(directory="images/"), name="images")
# api.mount("/", StaticFiles(directory="build/", html=True), name="build")


# @api.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors(), "Error": "Name field is missing"}),
#     )


# Run database migration
# Base.metadata.create_all(bind=engine)


# Specify the root route
# @api.get("/")
# async def redirect():
#     # Redirect to the docs route for now
#     return RedirectResponse("/docs")

# Add a sanity check route
@api.get("/ping")
def ping() -> str:
    return "pong"

# Wrap the FastAPI instance for AWS Lambda
handler = Mangum(api)

# Add logging
handler = logger.inject_lambda_context(handler, clear_state=True)
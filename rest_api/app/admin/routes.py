from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from ..utility import generate_unique_id
import os

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    generate_unique_id_function=generate_unique_id
)

@router.get("/env")
async def environment_variables() -> dict:
    # Redirect to the docs route for now
    return dict(os.environ)


# @router.get("/")
# async def redirect():
#     # Redirect to the docs route for now
#     return RedirectResponse("/docs")

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from ..utility import generate_unique_id


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    generate_unique_id_function=generate_unique_id
)


@router.get("/")
async def redirect():
    # Redirect to the docs route for now
    return RedirectResponse("/docs")

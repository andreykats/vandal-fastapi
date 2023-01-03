from fastapi import APIRouter, Depends, Form, File, UploadFile
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from ..dependencies import get_db


# Clean up verbose function names in Client Generator
def generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    generate_unique_id_function=generate_unique_id
)

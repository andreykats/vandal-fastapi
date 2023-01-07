from fastapi import FastAPI
from fastapi.routing import APIRoute
from typing import Callable


# Clean up verbose function names in Client Generator
def generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


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

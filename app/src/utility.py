from fastapi.routing import APIRoute, BaseRoute
from typing import Callable, cast

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit  # noqa: F401


logger: Logger = Logger()
# metrics: Metrics = Metrics()
# tracer: Tracer = Tracer()

# Clean up verbose function names in Client Generator
def generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


def update_schema_name(routes: list[BaseRoute], function: Callable, name: str) -> None:
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
    for base_route in routes:
        api_route = cast(APIRoute, base_route)  # Convert to APIRoute to access endpoint and the body_fiel attribute
        if api_route.endpoint is function:
            if api_route.body_field is None:
                break
            api_route.body_field.type_.__name__ = name
            break

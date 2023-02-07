from typing import Generator, Any

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.src.art.models_ddb import LayerTable
from app.src.live.models_ddb import MessageTable


@pytest.fixture(autouse=True)
def init_tables() -> Generator[None, None, None]:
    if not LayerTable.exists():
        LayerTable.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )

    if not MessageTable.exists():
        MessageTable.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )
    yield
    LayerTable.delete_table()
    MessageTable.delete_table()


@pytest.fixture
def app() -> FastAPI:
    from app.src.main import app as api_app
    return api_app


@pytest.fixture()
def client(app: FastAPI, init_tables: Any) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
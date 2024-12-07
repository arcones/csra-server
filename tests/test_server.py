import os
import pytest
from fastapi.testclient import TestClient

from csra_server.env import get_db_path
from csra_server.main import app


@pytest.fixture(scope="module", autouse=True)
def set_test_env():
    os.environ["ENV"] = "test"
    yield
    if os.path.exists(get_db_path()):
        os.remove(get_db_path())


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


def test_create_and_retrieve_task(client):
    create_response = client.post("/tasks/", json={"query_string": "Test query"})

    assert create_response.status_code == 200
    created_task = create_response.json()
    assert created_task["query_string"] == "Test query"
    assert created_task["status"] == "QUEUED"

    retrieve_response = client.get("/tasks/")
    assert retrieve_response.status_code == 200
    tasks = retrieve_response.json()
    assert len(tasks) > 0
    retrieved_task = tasks[0]
    assert retrieved_task["query_string"] == "Test query"
    assert retrieved_task["status"] == "QUEUED"

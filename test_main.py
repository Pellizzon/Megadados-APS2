from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)


def test_read_main_returns_not_found():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_get_whole_list():
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json() == {}  # list is always empty initially


def test_create_task():
    response = client.post(
        "/task", json={"description": "some description", "completed": "False"}
    )
    assert response.status_code == 200
    # TODO verify return value


def test_delete_invalid_task():
    uuid_ = uuid.uuid4()
    response = client.delete(f"/task/{uuid_}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_valid_task():
    response = client.post(
        "/task", json={"description": "some description", "completed": "False"}
    )
    assert response.status_code == 200

    response2 = client.delete(f"/task/{response.json()}")
    assert response2.status_code == 200
    assert response2.json() == None

from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)


def test_read_main_returns_not_found():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_create_task_and_delete_valid_task():
    # Create task to be deleted
    response = client.post(
        "/task", json={"description": "some description", "completed": "False"}
    )
    assert response.status_code == 200

    # Check if task works && avoid conflicts on further testing
    response2 = client.delete(f"/task/{response.json()}")
    assert response2.status_code == 200
    assert response2.json() == None


def test_delete_invalid_task():
    # Try to delete random uuid
    uuid_ = uuid.uuid4()
    response = client.delete(f"/task/{uuid_}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_get_valid_task():
    # Create task to get
    response = client.post(
        "/task", json={"description": "some description", "completed": "False"}
    )
    assert response.status_code == 200

    # Get task
    response2 = client.get(f"/task/{response.json()}")
    assert response2.status_code == 200
    assert response2.json() == {"description": "some description", "completed": False}

    # delete task to avoid mistakes on other tests
    response3 = client.delete(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == None


def test_get_invalid_task():
    # Get task with random UUID
    uuid_ = uuid.uuid4()
    response = client.get(f"/task/{uuid_}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_get_whole_list_when_empty():
    # Get list when empty
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json() == {}  # list is always empty initially


def test_get_whole_list():
    # Create a few tasks
    response1 = client.post(
        "/task", json={"description": "some description", "completed": "False"}
    )
    assert response1.status_code == 200
    response2 = client.post(
        "/task", json={"description": "another description", "completed": "False"}
    )
    assert response2.status_code == 200
    response3 = client.post(
        "/task", json={"description": "another description", "completed": "True"}
    )
    assert response3.status_code == 200

    # Get all tasks
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json() == {
        response1.json(): {
            "description": "some description",
            "completed": False,
        },
        response2.json(): {
            "description": "another description",
            "completed": False,
        },
        response3.json(): {
            "description": "another description",
            "completed": True,
        },
    }

    # delete tasks to avoid mistakes on other tests
    delete1 = client.delete(f"/task/{response1.json()}")
    assert delete1.status_code == 200
    assert delete1.json() == None
    delete2 = client.delete(f"/task/{response2.json()}")
    assert delete2.status_code == 200
    assert delete2.json() == None
    delete3 = client.delete(f"/task/{response3.json()}")
    assert delete3.status_code == 200
    assert delete3.json() == None


def test_get_completed_tasks():
    # Create a few tasks
    response1 = client.post(
        "/task", json={"description": "some description", "completed": "False"}
    )
    assert response1.status_code == 200
    response2 = client.post(
        "/task", json={"description": "another description", "completed": "False"}
    )
    assert response2.status_code == 200
    response3 = client.post(
        "/task", json={"description": "another description", "completed": "True"}
    )
    assert response3.status_code == 200

    # Get complete tasks
    response = client.get("/task?completed=true")
    assert response.status_code == 200
    assert response.json() == {
        response3.json(): {
            "description": "another description",
            "completed": True,
        },
    }

    # delete tasks to avoid mistakes on other tests
    delete1 = client.delete(f"/task/{response1.json()}")
    assert delete1.status_code == 200
    assert delete1.json() == None
    delete2 = client.delete(f"/task/{response2.json()}")
    assert delete2.status_code == 200
    assert delete2.json() == None
    delete3 = client.delete(f"/task/{response3.json()}")
    assert delete3.status_code == 200
    assert delete3.json() == None


def test_get_incomplete_tasks():
    # Create a few tasks
    response1 = client.post(
        "/task", json={"description": "some description", "completed": "False"}
    )
    assert response1.status_code == 200
    response2 = client.post(
        "/task", json={"description": "another description", "completed": "False"}
    )
    assert response2.status_code == 200
    response3 = client.post(
        "/task", json={"description": "another description", "completed": "True"}
    )
    assert response3.status_code == 200

    # Get incomplete tasks
    response = client.get("/task?completed=false")
    assert response.status_code == 200
    assert response.json() == {
        response1.json(): {
            "description": "some description",
            "completed": False,
        },
        response2.json(): {
            "description": "another description",
            "completed": False,
        },
    }

    # delete tasks to avoid mistakes on other tests
    delete1 = client.delete(f"/task/{response1.json()}")
    assert delete1.status_code == 200
    assert delete1.json() == None
    delete2 = client.delete(f"/task/{response2.json()}")
    assert delete2.status_code == 200
    assert delete2.json() == None
    delete3 = client.delete(f"/task/{response3.json()}")
    assert delete3.status_code == 200
    assert delete3.json() == None


def test_patch_valid_task():
    # create task
    response = client.post(
        "/task", json={"description": "some description", "completed": "False"}
    )
    assert response.status_code == 200

    # patch task
    response2 = client.patch(
        f"/task/{response.json()}",
        json={"description": "another description", "completed": "True"},
    )
    assert response2.status_code == 200
    assert response2.json() == None

    # verify if patch worked
    response3 = client.get(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == {
        "description": "another description",
        "completed": True,
    }

    # delete task to avoid mistakes on other tests
    response4 = client.delete(f"/task/{response.json()}")
    assert response2.status_code == 200
    assert response2.json() == None


def test_patch_invalid_task():
    # Try to patch given a random uuid
    uuid_ = uuid.uuid4()
    response = client.patch(
        f"/task/{uuid_}", json={"description": "some description", "completed": "False"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_put_valid_task():
    # create task
    response = client.post(
        "/task", json={"description": "some description", "completed": "False"}
    )
    assert response.status_code == 200

    # replace task
    response2 = client.put(
        f"/task/{response.json()}",
        json={"description": "another description", "completed": "True"},
    )
    assert response2.status_code == 200
    assert response2.json() == None

    # verify if put worked
    response3 = client.get(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == {
        "description": "another description",
        "completed": True,
    }

    # delete task to avoid mistakes on other tests
    response4 = client.delete(f"/task/{response.json()}")
    assert response2.status_code == 200
    assert response2.json() == None


def test_put_invalid_uuid():
    # Try to replace given a random uuid
    invalid_uuid = "Not a UUID"
    response = client.put(
        f"/task/{invalid_uuid}", json={"description": "some description", "completed": "False"}
    )
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['path', 'uuid_'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}]}


def test_patch_invalid_uuid():
    # Try to patch given a random uuid
    invalid_uuid = "Not a UUID"
    response = client.patch(
        f"/task/{invalid_uuid}", json={"description": "some description", "completed": "False"}
    )
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['path', 'uuid_'], 'msg': 'value is not a valid uuid', 'type': 'type_error.uuid'}]}
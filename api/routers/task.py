# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import uuid
from typing import Dict
from fastapi import APIRouter, HTTPException, Depends
from api.models import Task
from api.database import get_db, DBSession

router = APIRouter()


@router.get(
    "",
    tags=["task"],
    summary="Reads task list",
    description="Reads the whole task list.",
    response_model=Dict[uuid.UUID, Task],
)
async def read_tasks(completed: bool = None, db: DBSession = Depends(get_db)):
    if completed is None:
        return db.readTaskList()
    else:
        return db.readTaskListByStatus(completed)


@router.post(
    "",
    tags=["task"],
    summary="Creates a new task",
    description="Creates a new task and returns its UUID.",
    response_model=uuid.UUID,
)
async def create_task(item: Task, db: DBSession = Depends(get_db)):
    uuid_ = uuid.uuid4()
    return db.createNewTask(uuid_, item)


@router.get(
    "/{uuid_}",
    tags=["task"],
    summary="Reads task",
    description="Reads task from UUID.",
    response_model=Task,
)
async def read_task(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        return db.readTask(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        ) from exception


@router.put(
    "/{uuid_}",
    tags=["task"],
    summary="Replaces a task",
    description="Replaces a task identified by its UUID.",
)
async def replace_task(uuid_: uuid.UUID, item: Task, db: DBSession = Depends(get_db)):
    try:
        db.replaceTask(uuid_, item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        ) from exception


@router.patch(
    "/{uuid_}",
    tags=["task"],
    summary="Alters task",
    description="Alters a task identified by its UUID",
)
async def alter_task(uuid_: uuid.UUID, item: Task, db: DBSession = Depends(get_db)):
    try:
        db.alterTask(uuid_, item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        ) from exception


@router.delete(
    "/{uuid_}",
    tags=["task"],
    summary="Deletes task",
    description="Deletes a task identified by its UUID",
)
async def remove_task(uuid_: uuid.UUID, db: DBSession = Depends(get_db)):
    try:
        db.deleteTask(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        ) from exception

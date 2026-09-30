from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    response_description="The newly created task record.",
)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task with a required **title** and an optional **description**.
    """
    return crud.create_task(db=db, task_in=task_in)


@router.get(
    "/",
    response_model=list[schemas.TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all tasks",
    response_description="A list of tasks matching optional filter criteria.",
)
def read_tasks(
    completed: Optional[bool] = Query(
        default=None,
        description="Filter tasks by completion status: `true` for completed, `false` for pending.",
    ),
    db: Session = Depends(get_db),
):
    """
    Retrieve all tasks with optional filter by completion status (`?completed=true` or `?completed=false`).
    Returns an empty list `[]` if no tasks exist or match the filter.
    """
    return crud.get_tasks(db=db, completed=completed)


@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a single task by ID",
    response_description="The requested task details.",
    responses={
        404: {
            "model": schemas.ErrorResponse,
            "description": "Task with specified ID was not found.",
        }
    },
)
def read_task(
    task_id: int = Path(..., description="The unique integer ID of the task", ge=1),
    db: Session = Depends(get_db),
):
    """
    Retrieve a single task by its unique ID.
    Raises **404 Not Found** if the task does not exist.
    """
    task = crud.get_task_by_id(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return task


@router.put(
    "/{task_id}",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing task",
    response_description="The updated task details.",
    responses={
        404: {
            "model": schemas.ErrorResponse,
            "description": "Task with specified ID was not found.",
        }
    },
)
def update_task(
    task_id: int = Path(..., description="The unique integer ID of the task", ge=1),
    task_in: schemas.TaskUpdate = ...,
    db: Session = Depends(get_db),
):
    """
    Update an existing task by ID.
    Allows updating `title`, `description`, or `is_completed`.
    Raises **404 Not Found** if the task does not exist.
    """
    db_task = crud.get_task_by_id(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return crud.update_task(db=db, db_task=db_task, task_in=task_in)


@router.patch(
    "/{task_id}/complete",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Mark a task as completed",
    response_description="The task with completion status set to true.",
    responses={
        404: {
            "model": schemas.ErrorResponse,
            "description": "Task with specified ID was not found.",
        }
    },
)
def mark_task_completed(
    task_id: int = Path(..., description="The unique integer ID of the task", ge=1),
    db: Session = Depends(get_db),
):
    """
    Mark a task as completed (`is_completed = true`) by ID.
    Raises **404 Not Found** if the task does not exist.
    """
    db_task = crud.get_task_by_id(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return crud.mark_task_completed(db=db, db_task=db_task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    response_description="Task successfully deleted. Returns empty response body.",
    responses={
        404: {
            "model": schemas.ErrorResponse,
            "description": "Task with specified ID was not found.",
        }
    },
)
def delete_task(
    task_id: int = Path(..., description="The unique integer ID of the task", ge=1),
    db: Session = Depends(get_db),
):
    """
    Delete a task by ID.
    Raises **404 Not Found** if the task does not exist.
    """
    db_task = crud.get_task_by_id(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    crud.delete_task(db=db, db_task=db_task)
    return None

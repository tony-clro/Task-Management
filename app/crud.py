from sqlalchemy.orm import Session
from app import models, schemas


def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    """Creates a new Task record in the database."""
    db_task = models.Task(**task_in.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, completed: bool | None = None) -> list[models.Task]:
    """Retrieves tasks from the database with an optional completion status filter."""
    query = db.query(models.Task)
    if completed is not None:
        query = query.filter(models.Task.is_completed == completed)
    return list(query.all())


def get_task_by_id(db: Session, task_id: int) -> models.Task | None:
    """Retrieves a single task by its ID."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(
    db: Session, db_task: models.Task, task_in: schemas.TaskUpdate
) -> models.Task:
    """Updates an existing task record with provided fields."""
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def mark_task_completed(db: Session, db_task: models.Task) -> models.Task:
    """Marks a task as completed."""
    db_task.is_completed = True
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, db_task: models.Task) -> None:
    """Deletes a task record from the database."""
    db.delete(db_task)
    db.commit()

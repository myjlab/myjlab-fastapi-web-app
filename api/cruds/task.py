from datetime import date

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session

import api.models.task as task_model
import api.schemas.task as task_schema


def create_task(
    db: Session, task_create: task_schema.TaskCreate
) -> task_model.Task:
    task = task_model.Task(**task_create.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(
    db: Session,
    task_id: int,
) -> task_model.Task | None:
    result: Result = db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    return result.scalars().first()


def get_task_with_done(
    db: Session,
    task_id: int,
) -> tuple[int, str, date, bool] | None:
    result: Result = db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Task.due_date,
            task_model.Done.id.isnot(None).label("done"),
        )
        .outerjoin(task_model.Done)
        .filter(task_model.Task.id == task_id)
    )
    return result.first()


def get_tasks_with_done(db: Session) -> list[tuple[int, str, date, bool]]:
    result: Result = db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Task.due_date,
            task_model.Done.id.isnot(None).label("done"),
        ).outerjoin(task_model.Done)
    )

    return result.all()


def update_task(
    db: Session,
    task_create: task_schema.TaskCreate,
    original: task_model.Task,
) -> task_model.Task:
    original.title = task_create.title
    db.add(original)
    db.commit()
    db.refresh(original)
    return original


def delete_task(db: Session, original: task_model.Task) -> None:
    db.delete(original)
    db.commit()

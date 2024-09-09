from model import model, schemas, database
from sqlalchemy.orm import Session
from util import util
from datetime import time


def get_user_of_shift_time(start_time_of_shift: time, end_time_of_shift: time):
    db = database.SessionLocal()
    users = (
        db.query(model.User)
        .filter(
            (model.User.start_work_time >= start_time_of_shift)
            & (model.User.end_work_time <= end_time_of_shift)
        )
        .all()
    )
    return users


def get_user_of_task_time(start_time_of_task: time, user_id: int):
    db = database.SessionLocal()
    user = (
        db.query(model.User)
        .filter(
            (model.User.id == user_id)
            & (model.User.start_work_time >= start_time_of_task)
            & (model.User.end_work_time <= start_time_of_task)
        )
        .first()
    )

    if not user:
        return False
    else:
        return True

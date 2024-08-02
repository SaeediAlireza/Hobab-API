from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session

from util import util

router = APIRouter(tags=["task"], prefix="/task")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_task(
    request: schemas.TaskAddRequest,
    db: Session = Depends(util.get_db),
):
    new_task = model.Task(
        description=request.description,
        shift_id=request.shift_id,
        pool_id=request.pool_id,
        Location_id=request.Location_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/all", response_model=List[schemas.TaskInfoResponse])
def get_all_quantities(db: Session = Depends(util.get_db)):
    quantities = db.query(model.Task).all()
    if not quantities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any quantities"
        )
    else:
        return quantities


@router.get("/{id}", response_model=schemas.TaskInfoResponse)
def get_task_by_id(id: int, db: Session = Depends(util.get_db)):
    task = db.query(model.Task).filter(model.Task.id == id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any task with the id {id}",
        )
    else:
        return task

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, desc

from util import util

router = APIRouter(tags=["shift"], prefix="/shift")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_shift(
    request: schemas.ShiftAddRequest,
    db: Session = Depends(util.get_db),
):
    new_shift = model.Shift(
        start_time=request.start_time,
        end_time=request.end_time,
        description=request.description,
        user_id=request.user_id,
    )
    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)
    return new_shift


@router.get("/all", response_model=List[schemas.ShiftInfoResponse])
def get_all_shifts(db: Session = Depends(util.get_db)):
    shifts = db.query(model.Shift).order_by(desc(model.Shift.id)).all()
    if not shifts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any shifts"
        )
    else:
        return shifts


@router.get("/{id}", response_model=schemas.ShiftInfoResponse)
def get_shift_by_id(id: int, db: Session = Depends(util.get_db)):
    shift = db.query(model.Shift).filter(model.Shift.id == id).first()
    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there isn't any shift with the id {id}",
        )
    else:
        return shift


@router.get("/delete/{Shift_id}")
def delete_shift_by_id(
    Shift_id: int,
    response: Response,
    db: Session = Depends(util.get_db),
):
    Shift = db.query(model.Shift).filter(model.Shift.id == Shift_id).first()
    if not Shift:
        response.status_code = status.HTTP_404_NOT_FOUND
    db.delete(Shift)
    db.commit()
    return {"detail": "Item deleted successfully"}

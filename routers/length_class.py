from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, desc

from util import util

router = APIRouter(tags=["length class"], prefix="/length-class")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_length_class(
    request: schemas.LengthAddRequest,
    db: Session = Depends(util.get_db),
):
    new_length_class = model.LengthClass(
        start_length=request.start_length, end_length=request.end_length
    )
    db.add(new_length_class)
    db.commit()
    db.refresh(new_length_class)
    return new_length_class


@router.get("/all", response_model=List[schemas.LengthInfoResponse])
def get_all_length_classes(db: Session = Depends(util.get_db)):
    length_classes = (
        db.query(model.LengthClass).order_by(desc(model.LengthClass.id)).all()
    )
    if not length_classes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="there is'nt any length class",
        )
    else:
        return length_classes


@router.get("/{id}", response_model=schemas.LengthInfoResponse)
def get_length_class_by_id(id: int, db: Session = Depends(util.get_db)):
    length_class = (
        db.query(model.LengthClass).filter(model.LengthClass.id == id).first()
    )
    if not length_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any length class with the id {id}",
        )
    else:
        return length_class

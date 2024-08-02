from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session

from util import util

router = APIRouter(tags=["weight class"], prefix="/weight-class")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_weight_class(
    request: schemas.WeightAddRequest,
    db: Session = Depends(util.get_db),
):
    new_weight_class = model.WeightClass(
        start_weight=request.start_weight, end_weight=request.end_weight
    )
    db.add(new_weight_class)
    db.commit()
    db.refresh(new_weight_class)
    return new_weight_class


@router.get("/all", response_model=List[schemas.WeightInfoResponse])
def get_all_weight_classes(db: Session = Depends(util.get_db)):
    Weight_classes = db.query(model.WeightClass).all()
    if not Weight_classes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="there is'nt any weight class",
        )
    else:
        return Weight_classes


@router.get("/{id}", response_model=schemas.WeightInfoResponse)
def get_weight_class_by_id(id: int, db: Session = Depends(util.get_db)):
    weight_class = (
        db.query(model.WeightClass).filter(model.WeightClass.id == id).first()
    )
    if not weight_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any weight class with the id {id}",
        )
    else:
        return weight_class

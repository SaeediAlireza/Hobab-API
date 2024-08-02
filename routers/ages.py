from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session

from util import util

router = APIRouter(tags=["ages"], prefix="/ages")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_ages(
    request: schemas.AgesAddReqest,
    db: Session = Depends(util.get_db),
):
    new_ages = model.Ages(start_age=request.start_age, end_age=request.end_age)
    db.add(new_ages)
    db.commit()
    db.refresh(new_ages)
    return new_ages


@router.get("/all", response_model=List[schemas.AgesInfoResponse])
def get_all_ages(db: Session = Depends(util.get_db)):
    ages = db.query(model.Ages).all()
    if not ages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any ages"
        )
    else:
        return ages


@router.get("/{id}", response_model=schemas.AgesInfoResponse)
def get_ages_by_id(id: int, db: Session = Depends(util.get_db)):
    age = db.query(model.Ages).filter(model.Ages.id == id).first()
    if not age:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any ages with the id {id}",
        )
    else:
        return age

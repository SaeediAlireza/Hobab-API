from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, desc

from util import util

router = APIRouter(tags=["fish breed"], prefix="/fish-breed")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_fish_breed(
    request: schemas.FishBreedAddRequest,
    db: Session = Depends(util.get_db),
):
    new_fish_breed = model.FishBreed(
        name=request.name,
        description=request.description,
    )
    db.add(new_fish_breed)
    db.commit()
    db.refresh(new_fish_breed)
    return new_fish_breed


@router.get("/all", response_model=List[schemas.FishBreedInfoResponse])
def get_all_fish_breedes(db: Session = Depends(util.get_db)):
    fish_breedes = db.query(model.FishBreed).order_by(desc(model.FishBreed.id)).all()
    if not fish_breedes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="there is'nt any fish breed",
        )
    else:
        return fish_breedes


@router.get("/{id}", response_model=schemas.FishBreedInfoResponse)
def get_fish_breed_by_id(id: int, db: Session = Depends(util.get_db)):
    fish_breed = db.query(model.FishBreed).filter(model.FishBreed.id == id).first()
    if not fish_breed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any fish breed with the id {id}",
        )
    else:
        return fish_breed

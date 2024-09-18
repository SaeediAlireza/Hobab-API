from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, desc

from util import util

router = APIRouter(tags=["caviar breed"], prefix="/caviar-breed")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_caviar_breed(
    request: schemas.CaviarBreedAddRequest,
    db: Session = Depends(util.get_db),
):
    new_caviar_breed = model.CaviarBreed(
        name=request.name,
        description=request.description,
    )
    db.add(new_caviar_breed)
    db.commit()
    db.refresh(new_caviar_breed)
    return new_caviar_breed


@router.get("/all", response_model=List[schemas.CaviarBreedInfoResponse])
def get_all_caviar_breedes(db: Session = Depends(util.get_db)):
    caviar_breedes = (
        db.query(model.CaviarBreed).order_by(desc(model.CaviarBreed.id)).all()
    )
    if not caviar_breedes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="there is'nt any caviar breed",
        )
    else:
        return caviar_breedes


@router.get("/{id}", response_model=schemas.CaviarBreedInfoResponse)
def get_caviar_breed_by_id(id: int, db: Session = Depends(util.get_db)):
    caviar_breed = (
        db.query(model.CaviarBreed).filter(model.CaviarBreed.id == id).first()
    )
    if not caviar_breed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any caviar breed with the id {id}",
        )
    else:
        return caviar_breed

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, desc

from util import util

router = APIRouter(tags=["fish"], prefix="/fish")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_fish(
    request: schemas.FishAddRequest,
    db: Session = Depends(util.get_db),
):
    new_fish = model.Fish(
        birth_of_fish=request.birth_of_fish,
        fish_breed_id=request.fish_breed_id,
    )
    db.add(new_fish)
    db.commit()
    db.refresh(new_fish)
    return new_fish


@router.get("/all", response_model=List[schemas.FishInfoResponse])
def get_all_quantities(db: Session = Depends(util.get_db)):
    quantities = db.query(model.Fish).order_by(desc(model.Fish.id)).all()
    if not quantities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any quantities"
        )
    else:
        return quantities


@router.get(
    "/all-fish-location-pooltype/", response_model=schemas.PoolFishLocationInfoResponse
)
def get_all_quantities(db: Session = Depends(util.get_db)):
    fishes = db.query(model.Fish).order_by(desc(model.Fish.id)).all()
    locations = db.query(model.Location).order_by(desc(model.Location.id)).all()
    pool_types = db.query(model.PoolType).order_by(desc(model.PoolType.id)).all()
    response = schemas.PoolFishLocationInfoResponse(
        pool_types=pool_types,
        locations=locations,
        fishes=fishes,
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any quantities"
        )
    else:
        return response


@router.get("/{id}", response_model=schemas.FishInfoResponse)
def get_fish_by_id(id: int, db: Session = Depends(util.get_db)):
    fish = db.query(model.Fish).filter(model.Fish.id == id).first()
    if not fish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any fish with the id {id}",
        )
    else:
        return fish

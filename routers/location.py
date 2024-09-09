from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, desc

from util import util

router = APIRouter(tags=["location"], prefix="/location")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_location(
    request: schemas.LocationAddRequest,
    db: Session = Depends(util.get_db),
):
    new_location = model.Location(description=request.description)
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location


@router.get("/all", response_model=List[schemas.LocationInfoResponse])
def get_all_quantities(db: Session = Depends(util.get_db)):
    quantities = db.query(model.Location).order_by(desc(model.Location.id)).all()
    if not quantities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any quantities"
        )
    else:
        return quantities


@router.get("/{id}", response_model=schemas.LocationInfoResponse)
def get_location_by_id(id: int, db: Session = Depends(util.get_db)):
    location = db.query(model.Location).filter(model.Location.id == id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any location with the id {id}",
        )
    else:
        return location

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session

from util import util

router = APIRouter(tags=["pool"], prefix="/pool")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_pool(
    request: schemas.PoolAddRequest,
    db: Session = Depends(util.get_db),
):
    new_pool = model.Pool(
        description=request.description,
        Location_id=request.location_id,
        fish_id=request.fish_id,
        pool_type_id=request.pool_type_id,
    )
    db.add(new_pool)
    db.commit()
    db.refresh(new_pool)
    return new_pool


@router.get("/all", response_model=List[schemas.PoolInfoResponse])
def get_all_quantities(db: Session = Depends(util.get_db)):
    quantities = db.query(model.Pool).all()
    if not quantities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any quantities"
        )
    else:
        return quantities


@router.get("/{id}", response_model=schemas.PoolInfoResponse)
def get_pool_by_id(id: int, db: Session = Depends(util.get_db)):
    pool = db.query(model.Pool).filter(model.Pool.id == id).first()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any pool with the id {id}",
        )
    else:
        return pool

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session

from util import util

router = APIRouter(tags=["pool type"], prefix="/pool-type")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_pool_type(
    request: schemas.PoolTypeAddRequest,
    db: Session = Depends(util.get_db),
):
    new_pool_type = model.PoolType(
        name=request.name,
        description=request.description,
    )
    db.add(new_pool_type)
    db.commit()
    db.refresh(new_pool_type)
    return new_pool_type


@router.get("/all", response_model=List[schemas.PoolTypeInfoResponse])
def get_all_pool_typees(db: Session = Depends(util.get_db)):
    pool_typees = db.query(model.PoolType).all()
    if not pool_typees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="there is'nt any pool type",
        )
    else:
        return pool_typees


@router.get("/{id}", response_model=schemas.PoolTypeInfoResponse)
def get_pool_type_by_id(id: int, db: Session = Depends(util.get_db)):
    pool_type = db.query(model.PoolType).filter(model.PoolType.id == id).first()
    if not pool_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any pool type with the id {id}",
        )
    else:
        return pool_type

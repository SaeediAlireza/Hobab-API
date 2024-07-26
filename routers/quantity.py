from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session

from util import util

router = APIRouter(tags=["quantity"], prefix="/quantity")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_quantity(
    request: schemas.QuantityAddRequest,
    db: Session = Depends(util.get_db),
):
    new_quantity = model.Quantity(name=request.name)
    db.add(new_quantity)
    db.commit()
    db.refresh(new_quantity)
    return new_quantity


@router.get("/all", response_model=List[schemas.QuantityInfoResponse])
def get_all_quantities(db: Session = Depends(util.get_db)):
    quanities = db.query(model.Quantity).all()
    if not quanities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any quantities"
        )
    else:
        return quanities


@router.get("/{id}", response_model=schemas.QuantityInfoResponse)
def get_quantity_by_id(id: int, db: Session = Depends(util.get_db)):
    quantity = db.query(model.Quantity).filter(model.Quantity.id == id).first()
    if not quantity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any quantity with the id {id}",
        )
    else:
        return quantity

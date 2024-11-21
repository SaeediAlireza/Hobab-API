from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, desc

from util import util


router = APIRouter(tags=["item"], prefix="/item")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_item(
    request: schemas.ItemAddRequest,
    db: Session = Depends(util.get_db),
):
    new_item = model.Item(
        name=request.name,
        count=request.count,
        limit=request.limit,
        quantity_id=request.quantity_id,
        categorie_id=request.categorie_id,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/all/{id}", response_model=List[schemas.ItemInfoResponse])
def get_all_items_by_categorie(id: int, db: Session = Depends(util.get_db)):
    items = (
        db.query(model.Item)
        .filter(model.Item.categorie_id == id)
        .order_by(desc(model.Item.id))
        .all()
    )

    return items


@router.get("/all", response_model=List[schemas.ItemInfoResponse])
def get_all_items(db: Session = Depends(util.get_db)):
    items = db.query(model.Item).order_by(desc(model.Item.id)).all()

    return items

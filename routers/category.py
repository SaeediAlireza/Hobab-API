from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session

from util import util
from sqlalchemy import update, desc


router = APIRouter(tags=["category"], prefix="/category")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_category(
    request: schemas.CategoryAddRequest,
    db: Session = Depends(util.get_db),
):
    new_category = model.Categorie(name=request.name)
    user_exist = (
        db.query(model.Categorie)
        .filter(model.Categorie.name == new_category.name)
        .first()
    )

    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user exists")
    else:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, desc

from util import util


router = APIRouter(tags=["sub category"], prefix="/sub-category")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_sub_category(
    request: schemas.SubCategoryAddRequest,
    db: Session = Depends(util.get_db),
):
    new_sub_category = model.SubCategorie(
        dom_categorie_id=request.dom_categorie_id,
        sub_categorie_id=request.sub_categorie_id,
    )
    user_exist = (
        db.query(model.SubCategorie)
        .filter(
            model.SubCategorie.sub_categorie_id == new_sub_category.sub_categorie_id
        )
        .first()
    )

    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user exists")
    else:
        db.add(new_sub_category)
        db.commit()
        db.refresh(new_sub_category)
        return new_sub_category

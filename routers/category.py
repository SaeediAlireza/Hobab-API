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


@router.get("/all", response_model=List[schemas.CategoryInfoResponse])
def get_all_categories(db: Session = Depends(util.get_db)):
    categories = db.query(model.Categorie).order_by(desc(model.Categorie.id)).all()
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any categorie"
        )
    else:
        return categories


@router.get("/{id}", response_model=schemas.CategoryInfoResponse)
def get_category_by_id(id: int, db: Session = Depends(util.get_db)):
    categorie = db.query(model.Categorie).filter(model.Categorie.id == id).first()
    if not categorie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any categorie with the id {id}",
        )
    else:
        return categorie

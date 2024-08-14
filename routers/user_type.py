from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Response

# from repository import user_type
from model import model, schemas
from sqlalchemy.orm import Session
from util import util


router = APIRouter(tags=["user type"], prefix="/user-type")


@router.post("/add")
def add_user_type(
    request: schemas.UserTypeAddRequest,
    # current_user: Annotated[schemas.UserInfo, Depends(util.get_current_user)],
    db: Session = Depends(util.get_db),
):
    new_user_type = model.UserType(name=request.name)
    db.add(new_user_type)
    db.commit()
    db.refresh(new_user_type)
    return new_user_type


@router.get("/all", response_model=List[schemas.UserTypeInfo])
def get_all_user_types(
    response: Response,
    db: Session = Depends(util.get_db),
):
    user_types = db.query(model.UserType).all()
    if not user_types:
        response.status_code = status.HTTP_404_NOT_FOUND
    return user_types


@router.get("/{user_type_id}", response_model=schemas.UserTypeInfo)
def get_user_type_by_id(
    user_type_id: int,
    response: Response,
    db: Session = Depends(util.get_db),
):
    user_type = (
        db.query(model.UserType).filter(model.UserType.id == user_type_id).first()
    )
    if not user_type:
        response.status_code = status.HTTP_404_NOT_FOUND
    return user_type


@router.put("update")
def update_user_type(
    response: Response,
    request: schemas.UserTypeUpdateRequest,
    db: Session = Depends(util.get_db),
):
    user_type = db.query(model.UserType).filter(model.User.id == request.id).first()
    if not user_type:
        response.status_code = status.HTTP_404_NOT_FOUND
    user_type.name = request.name

    db.commit()
    db.refresh(user_type)
    return user_type


@router.get("/delete/{user_type_id}")
def delete_user_type_by_id(
    user_type_id: int,
    response: Response,
    db: Session = Depends(util.get_db),
):
    user_type = (
        db.query(model.UserType).filter(model.UserType.id == user_type_id).first()
    )
    if not user_type:
        response.status_code = status.HTTP_404_NOT_FOUND
    db.delete(user_type)
    db.commit()
    return {"detail": "Item deleted successfully"}

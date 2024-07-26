from fastapi import APIRouter, HTTPException, status, Response

# from repository import user_type
from model import model, schemas
from sqlalchemy.orm import Session


def get_router(db: Session):

    router = APIRouter(tags=["usertype"], prefix="/usertype")

    @router.post("/add")
    def add_user_type(request: schemas.UserTypeAddRequest):
        new_user_type = model.UserType(name=request.name)
        db.add(new_user_type)
        db.commit()
        db.refresh(new_user_type)
        return new_user_type

    @router.get()
    def get_user_type_by_id(
        user_type_id,
        response: Response,
    ):
        user_type = (
            db.query(model.UserType).filter(model.UserType.id == user_type_id).first
        )
        if not user_type:
            response.status_code = status.HTTP_404_NOT_FOUND
        return user_type

    @router.get("/all")
    def get_all_user_types(
        response: Response,
    ):
        user_types = db.query(model.UserType).all()
        if not user_types:
            response.status_code = status.HTTP_404_NOT_FOUND
        return user_types

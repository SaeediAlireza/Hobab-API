from fastapi import APIRouter, HTTPException, status
from repository import user
from model import model, schemas
from sqlalchemy.orm import Session


def get_router(db: Session):

    router = APIRouter(tags=["user"], prefix="users")

    @router.post("/add", status_code=status.HTTP_201_CREATED)
    def add_user(
        request: schemas.UserAddRequest,
    ):
        new_user = model.User(
            user_name=request.user_name,
            password=request.password,
            name=request.name,
            user_type_id=request.user_type_id,
        )

        if user.exists(db):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="user exists"
            )
        else:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

    return router

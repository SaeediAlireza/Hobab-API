from fastapi import APIRouter, HTTPException, status, Response
from repository import user
from model import model, schemas
from sqlalchemy.orm import Session


def get_router(db: Session):

    router = APIRouter(tags=["user"], prefix="/users")

    @router.post("/add", status_code=status.HTTP_201_CREATED)
    def create_user(
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

    @router.get("/{type_id}")
    def get_users_by_type(
        type_id: int,
        response: Response,
    ):
        users = db.query(model.User).filter(model.User.user_type_id == type_id).all()
        if not users:
            response.status_code = status.HTTP_404_NOT_FOUND
        return users

    @router.get("/{user_id}")
    def get_user_by_id(
        user_id,
        response: Response,
    ):
        user = db.query(model.User).filter(model.User.id == user_id).first
        if not user:
            response.status_code = status.HTTP_404_NOT_FOUND
        return user

    @router.get("/all")
    def get_all_users(
        response: Response,
    ):
        users = db.query(model.User).all()
        if not users:
            response.status_code = status.HTTP_404_NOT_FOUND
        return users

    return router

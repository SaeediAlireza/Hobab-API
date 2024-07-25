from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, status
from sqlalchemy.orm import Session
from model import model, schemas
from util import util


def get_router():
    router = APIRouter(tags=["authenticaton"])

    @router.post("/login", response_model=schemas.Token)
    def login(
        request: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(util.get_db),
    ):
        user = (
            db.query(model.User)
            .filter(model.User.user_name == request.username)
            .first()
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="invalid username"
            )

        if not util.verify(user.password, request.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="invalid username"
            )
        access_token = util.create_access_token(data={"sub": user.user_name})
        return schemas.Token(access_token=access_token, token_type="bearer")

    return router

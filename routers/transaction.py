from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session

from util import util


router = APIRouter(tags=["sub category"], prefix="/sub-category")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_transaction(
    request: schemas.TransactionAddReqest,
    db: Session = Depends(util.get_db),
):
    new_item = model.Transaction(
        input=request.input,
        amount=request.amount,
        transaction_time=request.transaction_time,
        items_id=request.item_id,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

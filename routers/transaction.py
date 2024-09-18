from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, desc

from util import util


router = APIRouter(tags=["transaction"], prefix="/transacion")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_transaction(
    request: schemas.TransactionAddRequest,
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


@router.get("last", response_model=schemas.TransactionInfoResponse)
def get_last_transaction(
    response: Response,
    db: Session = Depends(util.get_db),
):
    last_transaction = (
        db.query(model.Transaction).order_by(model.Transaction.id.desc()).first()
    )
    if not last_transaction:
        response.status_code = status.HTTP_404_NOT_FOUND
    return last_transaction

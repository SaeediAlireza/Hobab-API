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
    # Update Item:
    item = db.query(model.Item).filter(model.Item.id == request.item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="the Item dose not exist"
        )
    if request.input:
        item.count = item.count + request.amount
    else:
        if item.count < request.amount:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="the Item dose not have that mutch amount",
            )
        item.count = item.count - request.amount
    db.commit()
    # transaction:
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


@router.get("/all", response_model=List[schemas.TransactionInfoResponse])
def get_all_transactions(db: Session = Depends(util.get_db)):
    transactions = (
        db.query(model.Transaction).order_by(desc(model.Transaction.id)).all()
    )
    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any Transactions"
        )
    else:
        return transactions


@router.get("/all/head", response_model=List[schemas.TransactionInfoResponse])
def get_last_15_transactions(db: Session = Depends(util.get_db)):
    transactions = (
        db.query(model.Transaction).order_by(desc(model.Transaction.id)).limit(15).all()
    )
    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any Transactions"
        )
    else:
        return transactions


@router.get("/{id}", response_model=schemas.TransactionInfoResponse)
def get_transaction_by_id(id: int, db: Session = Depends(util.get_db)):
    transaction = db.query(model.Transaction).filter(model.Transaction.id == id).first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any transaction with the id {id}",
        )
    else:
        return transaction


@router.get("/last", response_model=schemas.TransactionInfoResponse)
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

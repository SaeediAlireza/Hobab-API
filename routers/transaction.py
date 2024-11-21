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
    item = db.query(model.Item).filter(model.Item.id == request.items_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="the Item dose not exist"
        )
    item_amount = item.count
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
    db.refresh(item)
    # transaction:
    new_transaction = model.Transaction(
        input=request.input,
        amount=request.amount,
        transaction_time=request.transaction_time,
        items_id=request.items_id,
        user_id=request.user_id,
        last_amount=item_amount,
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    result = new_transaction
    if new_transaction.item.count < new_transaction.item.limit:
        new_alert = model.Alert(
            seen=False,
            alert_time=new_transaction.transaction_time,
            item_id=new_transaction.items_id,
        )
        db.add(new_alert)
        db.commit()

    return result


@router.get("/items", response_model=List[schemas.TransactionItemResponse])
def get_all_items_by_transaction(db: Session = Depends(util.get_db)):
    items = db.query(model.Item).order_by(desc(model.Item.id)).all()

    return items


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


@router.get("/by-item/{id}", response_model=List[schemas.TransactionInfoResponse])
def get_transactions_by_item_id(id: int, db: Session = Depends(util.get_db)):
    transactions = (
        db.query(model.Transaction)
        .order_by(desc(model.Transaction.id))
        .filter(model.Transaction.items_id == id)
        .all()
    )
    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any Transactions"
        )
    else:
        return transactions

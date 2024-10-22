from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, desc

from util import util


router = APIRouter(tags=["alert"], prefix="/alert")


@router.get("/all", response_model=List[schemas.AlertInfoResponse])
def get__all_not_seen_alerts(db: Session = Depends(util.get_db)):
    alerts = (
        db.query(model.Alert)
        .filter(model.Alert.seen == False)
        .order_by(desc(model.Alert.id))
        .all()
    )
    return alerts


@router.get("/{id}")
def seen_alerts(id: int, response: Response, db: Session = Depends(util.get_db)):
    alert = db.query(model.Alert).filter(model.Alert.id == id).first()
    if not alert:
        response.status_code = status.HTTP_404_NOT_FOUND

    alert.seen = True

    db.commit()
    db.refresh(alert)
    return alert

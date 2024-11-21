from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from model import model, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
import joblib
import numpy as np

from util import util

router = APIRouter(tags=["caviar"], prefix="/caviar")
beluga_model = joblib.load("beluga_model.pkl")


@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_caviar(
    request: schemas.CaviarAddRequest,
    db: Session = Depends(util.get_db),
):
    new_caviar = model.Caviar(
        weight=request.weight,
        length=request.length,
        time_of_birth=request.time_of_birth,
        weight_class_id=request.weight_class_id,
        length_class_id=request.length_class_id,
        ages_id=request.ages_id,
        pool_id=request.pool_id,
        caviar_breed_id=request.caviar_breed_id,
    )
    db.add(new_caviar)
    db.commit()
    db.refresh(new_caviar)
    return new_caviar


@router.get("/all", response_model=List[schemas.CaviarInfoResponse])
def get_all_quantities(db: Session = Depends(util.get_db)):
    quantities = db.query(model.Caviar).order_by(desc(model.Caviar.id)).all()
    if not quantities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is'nt any quantities"
        )
    else:
        return quantities


@router.get("/{id}", response_model=schemas.CaviarInfoResponse)
def get_caviar_by_id(id: int, db: Session = Depends(util.get_db)):
    caviar = db.query(model.Caviar).filter(model.Caviar.id == id).first()
    if not caviar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"there is't any caviar with the id {id}",
        )
    else:
        return caviar


@router.post("/predict")
def predict_weight(request: schemas.CaviarPredictionRequest):
    features = np.array([[request.age, request.length]])
    prediction = beluga_model.predict(features)
    return {"predicted_weight": prediction[0]}

from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.models import Deliveryman as DeliverymanModel
from app.database.connection import get_db
from app.schemas.deliveryman import DeliverymanResponse
from app.schemas.deliveryman import DeliverymanBase as DeliverymanRequest


router = APIRouter()


@router.get("", response_model=List[DeliverymanResponse])
def get_all_deliverymans(
    db: Session = Depends(get_db),
):
    return db.query(DeliverymanModel).all()


@router.get(
    "/{id_deliveryman}",
    response_model=DeliverymanResponse,
)
def get_deliveryman_by_id(
    id_deliveryman: int,
    db: Session = Depends(get_db),
):

    deliveryman_in_db = db.query(DeliverymanModel).get(id_deliveryman)
    if not deliveryman_in_db:
        raise HTTPException(status_code=404)

    return deliveryman_in_db


@router.post(
    "",
    response_model=DeliverymanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_deliveryman(
    deliveryman: DeliverymanRequest,
    db: Session = Depends(get_db),
):
    db_deliveryman = DeliverymanModel(
        name=deliveryman.name,
        vehicle=deliveryman.vehicle,
    )
    db.add(db_deliveryman)
    db.commit()

    return db_deliveryman


@router.put(
    "/{id_deliveryman}",
    response_model=DeliverymanResponse,
)
def update_deliveryman(
    id_deliveryman: int,
    deliveryman: DeliverymanRequest,
    db: Session = Depends(get_db),
):
    deliveryman_in_db = db.query(DeliverymanModel).get(id_deliveryman)
    if not deliveryman_in_db:
        raise HTTPException(status_code=404)

    deliveryman_in_db.name = deliveryman.name
    deliveryman_in_db.vehicle = deliveryman.vehicle
    db.commit()

    return deliveryman_in_db

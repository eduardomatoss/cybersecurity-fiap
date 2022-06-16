from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.models import Delivery as DeliveryModel
from app.database.connection import get_db
from app.schemas.delivery import DeliveryResponse
from app.schemas.delivery import DeliveryBase as DeliveryRequest


router = APIRouter()


@router.get("", response_model=List[DeliveryResponse])
def get_all_deliverys(
    db: Session = Depends(get_db),
):
    return db.query(DeliveryModel).all()


@router.get(
    "/{id_delivery}",
    response_model=DeliveryResponse,
)
def get_delivery_by_id(
    id_delivery: int,
    db: Session = Depends(get_db),
):

    delivery_in_db = db.query(DeliveryModel).get(id_delivery)
    if not delivery_in_db:
        raise HTTPException(status_code=404)

    return delivery_in_db


@router.post(
    "",
    response_model=DeliveryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_delivery(
    delivery: DeliveryRequest,
    db: Session = Depends(get_db),
):
    db_delivery = DeliveryModel(
        id_buyer=delivery.id_buyer,
        id_product=delivery.id_product,
        id_deliveryman=delivery.id_deliveryman,
        deliveryman_lat=delivery.deliveryman_lat,
        deliveryman_long=delivery.deliveryman_long,
        receiver_cpf=delivery.receiver_cpf,
        status_delivery=delivery.status_delivery,
    )
    db.add(db_delivery)
    db.commit()

    return db_delivery


@router.put(
    "/{id_delivery}",
    response_model=DeliveryResponse,
)
def update_delivery(
    id_delivery: int,
    delivery: DeliveryRequest,
    db: Session = Depends(get_db),
):
    delivery_in_db = db.query(DeliveryModel).get(id_delivery)
    if not delivery_in_db:
        raise HTTPException(status_code=404)

    delivery_in_db.id_buyer = delivery.id_buyer
    delivery_in_db.id_product = delivery.id_product
    delivery_in_db.id_deliveryman = delivery.id_deliveryman
    delivery_in_db.deliveryman_lat = delivery.deliveryman_lat
    delivery_in_db.deliveryman_long = delivery.deliveryman_long
    delivery_in_db.receiver_cpf = delivery.receiver_cpf
    delivery_in_db.status_delivery = delivery.status_delivery
    db.commit()

    return delivery_in_db


@router.get("/{id_buyer}/buyer", response_model=List[DeliveryResponse])
def get_delivery_by_buyer_id(id_buyer: int, db: Session = Depends(get_db)):
    delivery_in_db = db.query(DeliveryModel).filter_by(id_buyer=id_buyer).all()
    if delivery_in_db:
        return delivery_in_db
    raise HTTPException(status_code=404)

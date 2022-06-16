from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.models import Buyer as BuyerModel
from app.database.connection import get_db
from app.schemas.buyer import BuyerResponse
from app.schemas.buyer import BuyerBase as BuyerRequest


router = APIRouter()


@router.get("", response_model=List[BuyerResponse])
def get_all_buyers(
    db: Session = Depends(get_db),
):
    return db.query(BuyerModel).all()


@router.get(
    "/{id_buyer}",
    response_model=BuyerResponse,
)
def get_buyer_by_id(
    id_buyer: int,
    db: Session = Depends(get_db),
):

    buyer_in_db = db.query(BuyerModel).get(id_buyer)
    if not buyer_in_db:
        raise HTTPException(status_code=404)

    return buyer_in_db


@router.post(
    "",
    response_model=BuyerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_buyer(
    buyer: BuyerRequest,
    db: Session = Depends(get_db),
):
    db_buyer = BuyerModel(
        name=buyer.name,
        cpf=buyer.cpf,
        cep=buyer.cep,
        address_number=buyer.address_number,
        address_lat=buyer.address_lat,
        address_long=buyer.address_long,
    )
    db.add(db_buyer)
    db.commit()

    return db_buyer


@router.put(
    "/{id_buyer}",
    response_model=BuyerResponse,
)
def update_buyer(
    id_buyer: int,
    buyer: BuyerRequest,
    db: Session = Depends(get_db),
):
    buyer_in_db = db.query(BuyerModel).get(id_buyer)
    if not buyer_in_db:
        raise HTTPException(status_code=404)

    buyer_in_db.name = buyer.name
    buyer_in_db.cpf = buyer.cpf
    buyer_in_db.cep = buyer.cep
    buyer_in_db.address_number = buyer.address_number
    buyer_in_db.address_lat = buyer.address_lat
    buyer_in_db.address_long = buyer.address_long
    db.commit()

    return buyer_in_db

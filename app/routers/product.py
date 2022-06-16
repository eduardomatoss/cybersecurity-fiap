from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.models import Product as ProductModel
from app.database.connection import get_db
from app.schemas.product import ProductResponse
from app.schemas.product import ProductBase as ProductRequest


router = APIRouter()


@router.get("", response_model=List[ProductResponse])
def get_all_products(
    db: Session = Depends(get_db),
):
    return db.query(ProductModel).all()


@router.get(
    "/{id_product}",
    response_model=ProductResponse,
)
def get_product_by_id(
    id_product: int,
    db: Session = Depends(get_db),
):

    product_in_db = db.query(ProductModel).get(id_product)
    if not product_in_db:
        raise HTTPException(status_code=404)

    return product_in_db


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: ProductRequest,
    db: Session = Depends(get_db),
):
    db_product = ProductModel(
        name=product.name,
        value=product.value,
        quant=product.quant,
    )
    db.add(db_product)
    db.commit()

    return db_product


@router.put(
    "/{id_product}",
    response_model=ProductResponse,
)
def update_product(
    id_product: int,
    product: ProductRequest,
    db: Session = Depends(get_db),
):
    product_in_db = db.query(ProductModel).get(id_product)
    if not product_in_db:
        raise HTTPException(status_code=404)

    product_in_db.name = product.name
    product_in_db.value = product.value
    product_in_db.quant = product.quant
    db.commit()

    return product_in_db

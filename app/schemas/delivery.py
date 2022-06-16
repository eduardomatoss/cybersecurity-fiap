from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.buyer import BuyerResponse
from app.schemas.deliveryman import DeliverymanResponse
from app.schemas.product import ProductResponse


class DeliveryBase(BaseModel):
    id_buyer: int = Field(alias="idBuyer")
    id_product: int = Field(alias="idProduct")
    id_deliveryman: int = Field(alias="idDeliveryman")
    deliveryman_lat: float = Field(alias="deliverymanLat")
    deliveryman_long: float = Field(alias="deliverymanLong")
    receiver_cpf: str = Field(alias="receiverCpf")
    status_delivery: str = Field(alias="statusDelivery")


class DeliveryResponse(DeliveryBase):
    id: int
    buyer: Optional[BuyerResponse]
    deliveryman: Optional[DeliverymanResponse]
    product: Optional[ProductResponse]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

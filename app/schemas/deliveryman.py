from pydantic import BaseModel


class DeliverymanBase(BaseModel):
    name: str
    vehicle: str


class DeliverymanResponse(DeliverymanBase):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

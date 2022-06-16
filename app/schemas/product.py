from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    value: float
    quant: int


class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

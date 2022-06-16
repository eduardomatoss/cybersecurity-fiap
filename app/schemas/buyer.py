from pydantic import BaseModel, Field


class BuyerBase(BaseModel):
    name: str
    cpf: str
    cep: str
    address_number: int = Field(alias="addressNumber")
    address_lat: float = Field(alias="addressLat")
    address_long: float = Field(alias="addressLong")


class BuyerResponse(BuyerBase):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

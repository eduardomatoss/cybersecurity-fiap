from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

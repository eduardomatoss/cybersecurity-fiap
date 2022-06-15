from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.models import Users as UsersModel
from app.database.connection import get_db
from app.schemas.users import UserResponse
from app.schemas.users import UserBase as UserRequest


router = APIRouter()


@router.get("", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
):
    return db.query(UsersModel).all()


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserRequest,
    db: Session = Depends(get_db),
):
    db_user = UsersModel(name=user.name)
    db.add(db_user)
    db.commit()

    return db_user

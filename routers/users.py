
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserCreate, UserResponse
from crud import get_users
from services import create_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
    description="Creates a user and rejects duplicate email addresses."
)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db, data)


@router.get(
    "",
    response_model=list[UserResponse],
    summary="List all users"
)
def list_users(db: Session = Depends(get_db)):
    return get_users(db)

from app.exceptions import UserAlreadyExistsException
from app.users.utils import get_password_hash
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas import UserCreate, UserResponse,UserAuth
from app.users.crud import create_user, get_user_by_email
from app.users.auth import  authenticate_user, create_access_token
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, существует ли пользователь с таким email
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await create_user(
        db=db,
        email=user_data.email,
        hashed_password=hashed_password,
        name=user_data.name
    )
    return new_user


@router.post("/login")
async def login_user(response: Response, user_data: UserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token

from datetime import datetime, timedelta, timezone
from app.config import settings
from app.exceptions import IncorrectEmailOrPasswordException
from app.users.crud import get_user_by_email
from app.users.utils import verify_password
from pydantic import EmailStr
import jwt



def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await get_user_by_email(email)
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectEmailOrPasswordException
    return user
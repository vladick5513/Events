import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from fastapi import Depends, Request
from app.config import settings
from app.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.crud import get_user_by_id

def get_token(request: Request) -> str:
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except InvalidTokenError:
        raise IncorrectTokenFormatException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user = await get_user_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
from app.database import async_session_factory
from app.users.schemas import UserCreate
from app.users.utils import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.users.models import User

async def get_user_by_email(email: str) -> User | None:
    async with async_session_factory() as session:
        query = select(User).filter(User.email == email)
        result = await session.execute(query)
        return result.scalars().first()

async def get_user_by_id(user_id: int) -> User | None:
    async with async_session_factory() as session:
        query = select(User).filter(User.id == user_id)
        result = await session.execute(query)
        return result.scalars().first()

async def create_user(db: AsyncSession, email: str, hashed_password: str, name: str = None) -> User:
    user = User(name=name, email=email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # Обновляем объект после сохранения
    return user


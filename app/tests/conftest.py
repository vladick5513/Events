import asyncio
import uuid
import pytest
from app.config import settings
from app.database import Base, async_session_factory, async_engine
from app.main import app
from app.users.models import User
from app.bookings.models import Booking
from app.events.models import Event
from app.users.utils import get_password_hash
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def create_test_user():
    async with async_session_factory() as session:
        email = f"{uuid.uuid4()}@example.com"
        hashed_password = get_password_hash("password123")
        user = User(email=email, name="Test User", hashed_password=hashed_password)
        session.add(user)
        await session.commit()
        return {"email": email, "password": "password123"}

@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

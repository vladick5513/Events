from datetime import date
from app.events.schemas import EventCreate
from app.exceptions import TitleNotFoundException, DateNotFoundException, InvalidDateException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.events.models import Event


async def create_event(db: AsyncSession, event_data: EventCreate):
    event = Event(**event_data.dict())
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event

async def get_event_by_id(db: AsyncSession, event_id: int):
    result = await db.execute(select(Event).where(Event.id == event_id))
    return result.scalar()


async def get_all_events(db: AsyncSession, title: str = None, event_date: date = None):
    query = select(Event)

    if title:
        query = query.where(Event.title == title)
    if event_date:
        query = query.where(Event.date == event_date)

    result = await db.execute(query)
    events = result.scalars().all()

    if not events:
        if title and event_date:
            raise TitleNotFoundException
        elif title:
            raise TitleNotFoundException
        elif event_date:
            raise DateNotFoundException

    return events

async def update_event(db: AsyncSession, event_id: int, update_data):
    event = await get_event_by_id(db, event_id)
    if not event:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(event, key, value)
    await db.commit()
    await db.refresh(event)
    return event

async def delete_event(db: AsyncSession, event_id: int):
    event = await get_event_by_id(db, event_id)
    if not event:
        return None
    await db.delete(event)
    await db.commit()
    return event
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.events.schemas import EventCreate, EventUpdate, EventResponse
from app.events.crud import (
    create_event,
    get_event_by_id,
    get_all_events,
    update_event,
    delete_event
)
from app.database import get_db


router = APIRouter()

@router.post("", response_model=EventResponse)
async def create_event_route(
    event_data: EventCreate = Body(...),  # Body обеспечивает обязательность
    db: AsyncSession = Depends(get_db)
):
    return await create_event(db, event_data)


@router.get("/optional", response_model=list[EventResponse])
async def get_events(
    title: Optional[str] = Query(None, description="Search by event title"),
    event_date: Optional[date] = Query(None, description="Filter by exact date (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
):
    events = await get_all_events(db, title=title, event_date=event_date)
    return events


@router.get("/{event_id}", response_model=EventResponse)
async def get_event_route(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

@router.get("", response_model=list[EventResponse])
async def get_all_events_route(db: AsyncSession = Depends(get_db)):
    return await get_all_events(db)


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    db: AsyncSession = Depends(get_db)
):
    existing_event = await get_event_by_id(db, event_id)
    if not existing_event:
        raise HTTPException(status_code=404, detail="Event not found")

    for field, value in event_data.dict(exclude_unset=True).items():
        setattr(existing_event, field, value)

    db.add(existing_event)
    await db.commit()
    await db.refresh(existing_event)
    return existing_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event_route(event_id: int, db: AsyncSession = Depends(get_db)):
    event = await delete_event(db, event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return
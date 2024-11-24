from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime

class EventBase(BaseModel):
    title: str
    description: str
    date: date
    available_seats: int

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    date: Optional[date]
    available_seats: Optional[int]

class EventResponse(EventBase):
    id: int
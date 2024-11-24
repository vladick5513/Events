from pydantic import BaseModel

class BookingBase(BaseModel):
    event_id: int
    seats: int

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    user_id: int
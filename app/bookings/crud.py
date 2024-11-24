from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.bookings.models import Booking
from app.events.models import Event

async def create_booking(db: AsyncSession, user_id: int, booking_data):
    event = await db.execute(select(Event).where(Event.id == booking_data.event_id))
    event = event.scalar()
    if not event or event.available_seats < booking_data.seats:
        return None
    booking = Booking(user_id=user_id, **booking_data.dict())
    event.available_seats -= booking_data.seats
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking

async def get_bookings_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Booking).where(Booking.user_id == user_id))
    return result.scalars().all()

async def delete_booking(db: AsyncSession, booking_id: int, user_id: int):
    result = await db.execute(select(Booking).where(Booking.id == booking_id, Booking.user_id == user_id))
    booking = result.scalar()
    if not booking:
        return None

    event = await db.execute(select(Event).where(Event.id == booking.event_id))
    event = event.scalar()
    if event:
        event.available_seats += booking.seats

    await db.delete(booking)
    await db.commit()
    return booking
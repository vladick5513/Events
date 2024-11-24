from app.users.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.bookings.schemas import BookingCreate, BookingResponse
from app.bookings.crud import create_booking, get_bookings_by_user, delete_booking
from app.database import get_db

router = APIRouter()

@router.post("", response_model=BookingResponse)
async def create_booking_route(
    booking_data: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    booking = await create_booking(db, user_id=current_user.id, booking_data=booking_data)
    if not booking:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to create booking")
    return booking

@router.get("", response_model=list[BookingResponse])
async def get_bookings_route(db: AsyncSession = Depends(get_db),current_user= Depends(get_current_user)):
    return await get_bookings_by_user(db, user_id=current_user.id)

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking_route(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    booking = await delete_booking(db, booking_id=booking_id, user_id=current_user.id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return
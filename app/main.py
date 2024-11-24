from fastapi import FastAPI
from app.users.routers import router as user_router
from app.events.routers import router as event_router
from app.bookings.routers import router as booking_router



app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(event_router, prefix="/events", tags=["Events"])
app.include_router(booking_router, prefix="/bookings", tags=["Bookings"])

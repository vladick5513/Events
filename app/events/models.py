from app.database import Base
from sqlalchemy import Column, Integer, String, Text, Date

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    available_seats = Column(Integer, nullable=False)
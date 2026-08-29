from datetime import datetime, timezone 
from sqlalchemy import Column , Integer , String , DateTime , ForeignKey

from app.database import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True , index=True)
    name =Column(String , nullable=False)
    email = Column(String , unique=True , index=True, nullable=False)
    hashed_password = Column(String , nullable=False)
    role= Column(String,default ="attendee")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc)
    )
class Event(Base):
    __tablename__ ="events"
    id= Column(Integer , primary_key =True , index=True)
    organizer_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    title = Column(String , nullable=False)
    description=Column(String,nullable=True)
    location=Column(String, nullable=True)

    starts_at= Column(DateTime(timezone=True), nullabel =False)
    total_tickets=Column(Integer , nullable= False)
    available_ticekts=Column(Integer, nullable=False)

    status = Column(String, default="published")

    created_at = Column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc)

    )
class Ticket(Base):
    __tablename__ ="tickets"

    id = Column(Integer , primary_key=True, index=True)
    user_id = Column(Integer , ForeignKey("users.id"), nullable=False)
    event_id =Column(Integer, ForeignKey("events.id"), nullable =False)
    ticket_code = Column(String , unique=True , index =True , nullable=False)
    status = Column(String , default="valid")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)

    )
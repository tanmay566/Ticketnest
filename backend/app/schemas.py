from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr , Field , ConfigDict

#Auth Schemas 

class UserCreate(BaseModel):
    name:str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    role : Literal["attendee", "Organizer" ] = "attendee"

class UserOut(BaseModel):
    id:int 
    name:str
    email:EmailStr
    role:str
    created_at :datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token:str
    token_type:str ="bearer"

#Event Schemas

class EventCreate(BaseModel):
    title: str = Field(min_length=3 , max_length=200)
    description: str | None = None
    location : str | None = None
    starts_at: datetime
    total_tickets : int = Field (gt=0 , le=100000)

class EventOut(BaseModel):
    id : int
    organizer_id: int 
    title :str
    description: str | None
    location : str | None
    starts_at:datetime
    total_tickets :int
    available_tickets : int
    status : str 
    created_at :datetime
    model_config = ConfigDict(from_attributes=True)


#booking schmeas 

class BookingRequest(BaseModel):
    quantity : int  = Field(default=1 ,gt  =0 , le =5)

class TicketOut(BaseModel):
    id: int
    user_id :int
    event_id : int
    ticket_code: str
    status: str
    created_at : datetime 
    model_config = ConfigDict(from_attributes=True)
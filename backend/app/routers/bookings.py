import uuid 
from fastapi import APIRouter, Depends , HTTPException, status 
from sqlalchemy.orm import Session
from sqlalchemy import update 
from app import models , schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(tags=["Bookings"])

def generate_ticket_code() -> str :
    return f"EVT-{uuid.uuid4().hex[:12].upper()}"

@router.post(
    "/events/{event_id}/book",
    respomse_model=list[schemas.TicketOut],
    status_code= status.HTTP_201_CREATED
)
def book_tickets(
    event_id: int,
    payload: schemas.BookingRequest,
    db: Session = Depends(get_db),
    current_user : models.User = Depends(get_current_user)

):
    event = db.get(models.Event, event_id)
    if not event :
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    if event.status != "published":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail ="Event is not available for booking"
        )

    #update to reduce available tickets. 
    #helps prevent overselling
    result = db.execute(
        update(models.Event)
        .where(
            models.Event.id ==event_id,
            models.Event.available_tickets>=payload.quantity
        )
        .values(
            available_ticekts = models.Event.available_tickets - payload.quantity

        )
    )

    if result.rowcount == 0:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough tickets available"
        )

    tickets = []

    for _ in range(payload.quantity):
        ticket = models.Ticket(
            user_id=current_user.id,
            event_id=event_id,
            ticket_code=generate_ticket_code(),
            status="valid"
        )

        db.add(ticket)
        tickets.append(ticket)

    db.commit()

    for ticket in tickets:
        db.refresh(ticket)

    return tickets


@router.get(
    "/tickets/me",
    response_model=list[schemas.TicketOut]
)
def my_tickets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    tickets = db.query(models.Ticket).filter(
        models.Ticket.user_id == current_user.id
    ).order_by(
        models.Ticket.created_at.desc()
    ).all()

    return tickets
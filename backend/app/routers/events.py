from fastapi import APIRouter , Depends, HTTPException , status 
from sqlalchemy.orm import Session
from app import models , schemas
from app.database import get_db
from app.dependencies import get_current_organizer

router = APIRouter(prefix="/events", tags = ["Events"])

@router.post(
    "/",
    response_model = schemas.EventOut,
    status= status.HTTP_201_CREATED
)
def create_event(
    payload: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user :models.User = Depends(get_current_organizer)
):
    event = models. Event(
        organizer_id = current_user.id, 
        title =payload.title,
        description = payload.description,
        location =payload.location,
        starts_at = payload.starts_at,
        total_tickets =payload.total_tickets,
        available_tickets = payload.total_tickets,
        status ="published"
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event
@router.get("/", response_model=list[schemas.EventOut])
def list_events(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    events = db.query(models.Event).filter(
        models.Event.status == "published"
    ).order_by(
        models.Event.created_at.desc()
    ).offset(skip).limit(limit).all()

    return events


@router.get("/{event_id}", response_model=schemas.EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.get(models.Event, event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return event
@router.get("/", response_model=list[schemas.EventOut])
def list_events(
    skip:int =0, 
    limit: int = 10,
    db:Session = Depends(get_db)
):
    events = db.query(models.Event).filter(
        models.Event.status == "published"
    ).order_by(
        models.Event.created_at.desc()

    ).offset(skip).limit(limit).all()
    return events
@router.get("/{event_id}", response_model=schemas.EventOut)
def get_event(event_id: int , db: Session = Depends(get_db)):
    event = db.get(models.Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail ="Event not found"
        )
    return event 

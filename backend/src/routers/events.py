from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from core.db_utils import Events, Event_Create, Event_Update, Event_Response, get_db, User
from core.api_utils import check_if_registered, create_item, update_item
from core.oauth_utils import get_current_active_user


router = APIRouter(
    prefix="/events"
)



@router.post("/", response_model=Event_Response, status_code=status.HTTP_201_CREATED)
def create_event(event: Event_Create, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    check_if_registered(db, Events, Events.event_description, event.event_description, 400, "Event already registered")

    return create_item(Events, event, db)


@router.get("/all", response_model=List[Event_Response])
def get_events(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    return db.query(Events).all()


@router.get("/{event_id}", response_model=Event_Response)
def get_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    
    event = check_if_registered(db, Events, Events.event_id, event_id, 404, "Event not found", not_void=True)

    return event


@router.put("/{event_id}", response_model=Event_Response)
def update_event(event_id: int, event: Event_Update, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    event_data = check_if_registered(db, Events, Events.event_id, event_id, 404, "Event not found", not_void=True)

    update_item(db, event, event_data)

    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    event_data = check_if_registered(db, Events, Events.event_id, event_id, 404, "Event not found", not_void=True)

    db.delete(event_data)
    db.commit()

    return {"Event": "Deleted!"}


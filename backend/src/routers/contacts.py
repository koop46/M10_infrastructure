from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from core.db_utils import Contacts, Contact_Create, Contact_Update, Contact_Response, get_db, User
from core.api_utils import check_if_registered, create_item, update_item
from core.oauth_utils import get_current_active_user


router = APIRouter(
    prefix="/contacts"
)



@router.post("/", response_model=Contact_Response, status_code=status.HTTP_201_CREATED)
def create_contact(contact: Contact_Create, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    check_if_registered(db, Contacts, Contacts.contact_email, contact.contact_email, 400, "Contact already registered")

    return create_item(Contacts, contact, db)


@router.get("/all", response_model=List[Contact_Response])
def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    return db.query(Contacts).all()


@router.get("/{contact_id}", response_model=Contact_Response)
def get_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    contact = check_if_registered(db, Contacts, Contacts.contact_id, contact_id, 404, "Contact not found", not_void=True)

    return contact


@router.put("/{contact_id}", response_model=Contact_Response)
def update_contact(contact_id: int, contact: Contact_Update, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    contact_data = check_if_registered(db, Contacts, Contacts.contact_id, contact_id, 404, "Contact not found", not_void=True)

    update_item(db, contact, contact_data)

    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    contact_data = check_if_registered(db, Contacts, Contacts.contact_id, contact_id, 404, "Contact not found", not_void=True)

    db.delete(contact_data)
    db.commit()
    
    return {"Contact": "Deleted!"}

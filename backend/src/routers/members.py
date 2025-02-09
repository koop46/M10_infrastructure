from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from core.db_utils import Members, Member_Create, Member_Update, Member_Response, get_db, User
from core.api_utils import check_if_registered, create_item, update_item
from core.oauth_utils import get_current_active_user


router = APIRouter(
    prefix="/members"
    )



@router.post("/", response_model=Member_Response, status_code=status.HTTP_201_CREATED)
def create_member(member: Member_Create, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    check_if_registered(db, Members, Members.email, member.email, 400, "Member already registered")

    return create_item(Members, member, db)


@router.get("/all", response_model=List[Member_Response])
def get_members(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    return db.query(Members).all()


@router.get("/{member_id}", response_model=Member_Response)
def get_member(member_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    member = check_if_registered(db, Members, Members.member_id, member_id, 404, "Member not found", not_void=True)

    return member


@router.put("/{member_id}", response_model=Member_Response)
def update_member(member_id: int, member: Member_Update, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    member_data = check_if_registered(db, Members, Members.member_id, member_id, 404, "Member not found", not_void=True)
    update_item(db, member, member_data)

    return member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    member_data = check_if_registered(db, Members, Members.member_id, member_id, 404, "Member not found", not_void=True)
    db.delete(member_data)
    db.commit()
    
    return {"Member": "Deleted!"}

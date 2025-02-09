from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from core.db_utils import User, User_Create, User_Update, User_Response, get_db
from core.api_utils import check_if_registered, create_item, update_item
from core.oauth_utils import get_current_active_user



router = APIRouter(
    prefix="/users"
)



@router.post("/", response_model=User_Response, status_code=status.HTTP_201_CREATED)
def create_user(user: User_Create, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    check_if_registered(db, User, User.username, user.username, 400, "Username already registered")

    return create_item(User, user, db)


@router.get("/all", response_model=List[User_Response])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    return db.query(User).all()


@router.get("/{user_id}", response_model=User_Response)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    user = check_if_registered(db, User, User.user_id, user_id, 404, "User not found", not_void=True)

    return user


@router.put("/{user_id}", response_model=User_Response)
def update_user(user_id: int, user: User_Update, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    
    user_data = check_if_registered(db, User, User.user_id, user_id, 404, "User not found", not_void=True)
    update_item(db, user, user_data)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    user_data = check_if_registered(db, User, User.user_id, user_id, 404, "User not found", not_void=True)
    db.delete(user_data)
    db.commit()
    
    return {"User": "Deleted!"}

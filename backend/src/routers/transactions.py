from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from core.db_utils import Transactions, Transaction_Create, Transaction_Update, Transaction_Response, get_db, User
from core.api_utils import check_if_registered, create_item, update_item
from core.oauth_utils import get_current_active_user


router = APIRouter(
    prefix="/transactions"
    )



@router.post("/", response_model=Transaction_Response, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: Transaction_Create, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    check_if_registered(db, Transactions, Transactions.product_name, transaction.product_name, 400, "Transaction already registered")

    return create_item(Transactions, transaction, db)


@router.get("/all", response_model=List[Transaction_Response])
def get_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    return db.query(Transactions).all()


@router.get("/{transaction_id}", response_model=Transaction_Response)
def get_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    transaction = check_if_registered(db, Transactions, Transactions.transaction_id, transaction_id, 404, "Transaction not found", not_void=True)

    return transaction


@router.put("/{transaction_id}", response_model=Transaction_Response)
def update_transaction(transaction_id: int, transaction: Transaction_Update, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    transaction_data = check_if_registered(db, Transactions, Transactions.transaction_id, transaction_id, 404, "Transaction not found", not_void=True)

    update_item(db, transaction, transaction_data)
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):

    transaction_data = check_if_registered(db, Transactions, Transactions.transaction_id, transaction_id, 404, "Transaction not found", not_void=True)

    db.delete(transaction_data)
    db.commit()
    
    return {"Transaction": "Deleted!"}

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from core.db_utils import Companies, Company_Create, Company_Update, Company_Response, get_db, User
from core.api_utils import check_if_registered, create_item, update_item
from core.oauth_utils import get_current_active_user


router = APIRouter(
    prefix="/companies"
)



@router.post("/", response_model=Company_Response, status_code=status.HTTP_201_CREATED)
def create_company(company: Company_Create, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    check_if_registered(db, Companies, Companies.company_name, company.company_name, 400, "Company already registered")
    return create_item(Companies, company, db)

@router.get("/all", response_model=List[Company_Response])
def get_companies(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return db.query(Companies).all()

@router.get("/{company_id}", response_model=Company_Response)
def get_company(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    company = check_if_registered(db, Companies, Companies.company_id, company_id, 404, "Company not found", not_void=True)
    return company

@router.put("/{company_id}", response_model=Company_Response)
def update_company(company_id: int, company: Company_Update, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    company_data = check_if_registered(db, Companies, Companies.company_id, company_id, 404, "Company not found", not_void=True)
    update_item(db, company, company_data)
    return company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    company_data = check_if_registered(db, Companies, Companies.company_id, company_id, 404, "Company not found", not_void=True)
    db.delete(company_data)
    db.commit()
    return {"Company": "Deleted!"}

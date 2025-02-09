from sqlalchemy.orm import Session
from fastapi import HTTPException


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def check_if_registered(db, column_class, column_class_attribute, base_class_attribute, code, error_message, not_void=False):
    
    db_item = db.query(column_class).filter(column_class_attribute == base_class_attribute).first()

    if db_item and not not_void:
        print(error_message)
        raise HTTPException(status_code=code, detail=error_message)
    

    elif not db_item and not_void:
        print(error_message)
        raise HTTPException(status_code=code, detail=error_message)
    
    
    else:
        return db_item


def create_item(column_class, item_base_class, session: Session):

    new_item = column_class(**item_base_class.model_dump(exclude_none=True))
    session.add(new_item)
    session.commit()
    session.refresh(new_item)

    return new_item


def update_item(db, item_base_class, new_data):
      
    for key, value in item_base_class.model_dump().items():
        setattr(new_data, key, value)

    db.commit()
    db.refresh(new_data)
   

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



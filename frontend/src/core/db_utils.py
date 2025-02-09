from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from pydantic import BaseModel, model_validator
from typing import Optional
from sqlalchemy import ForeignKey



class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "User"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_password: Mapped[str] = mapped_column(nullable=False, unique=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False, unique=False)
    access_level: Mapped[int] = mapped_column(nullable=False, unique=False)
    disabled: Mapped[bool] = mapped_column(nullable=True, unique=False)
    
class User_Base(BaseModel):
    
    username: str
    user_password: str
    hashed_password: str
    access_level: int
    disabled: Optional[bool] = None


class User_Create(User_Base):
    pass


class User_Update(User_Base):
    user_id: int


class User_Response(User_Base):
    user_id: int

    class Config:
        from_attributes = True


class User_in_db(BaseModel):
    user_id: int
    username: str
    access_level: int
    hashed_password: str
    disabled: Optional[bool] = None 



###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  


class Companies(Base):

    __tablename__ = "Companies"

    company_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    company_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    company_email: Mapped[str] = mapped_column(nullable=False, unique=True)
    company_phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    industry: Mapped[str] = mapped_column(nullable=True, unique=False)
    internship: Mapped[bool] = mapped_column(nullable=False, unique=False)  # Corrected spelling of "internship"


class Company_Base(BaseModel):

    company_name: str
    company_email: str
    company_phone_number: str
    industry: Optional[str] = None
    internship: bool


class Company_Create(Company_Base):
    pass


class Company_Update(Company_Base):
    company_id: int


class Company_Response(Company_Base):
    company_id: int

    class Config:
        from_attributes = True



###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  


class Contacts(Base):

    __tablename__ = "Contacts"

    contact_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    contact_email: Mapped[str] = mapped_column(nullable=False, unique=False)
    contact_name: Mapped[str] = mapped_column(nullable=False, unique=False)
#    event_id: Mapped[int] = mapped_column(nullable=True, unique=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("Events.event_id"), nullable=False)
    contact_channel: Mapped[str] = mapped_column(nullable=True, unique=False)

    event: Mapped["Events"] = relationship("Events", back_populates="contacts")


class Contact_Base(BaseModel):

    contact_email: str
    contact_name: str
    event_id: int  # Foreign key to Events
    contact_channel: Optional[str] = None


class Contact_Create(Contact_Base):
    pass


class Contact_Update(Contact_Base):
    contact_id: int


class Contact_Response(Contact_Base):
    contact_id: int

    class Config:
        from_attributes = True




###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  



class Events(Base):

    __tablename__ = "Events"
    
    event_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    event_description: Mapped[str] = mapped_column(nullable=False, unique=True)
    event_date: Mapped[str] = mapped_column(nullable=False, unique=True)  
    contacts: Mapped[list["Contacts"]] = relationship("Contacts", back_populates="event")  # One-to-many relationship
    event_cost: Mapped[float] = mapped_column(nullable=False, unique=False)
    event_partners: Mapped[str] = mapped_column(nullable=True, unique=False)

    contacts: Mapped[list["Contacts"]] = relationship("Contacts", back_populates="event")


class Event_Base(BaseModel):

    event_description: str
    event_date: str
    event_cost: float
    event_partners: Optional[str] = None


class Event_Create(Event_Base):
    pass


class Event_Update(Event_Base):
    event_id: int


class Event_Response(Event_Base):
    event_id: int

    class Config:
        from_attributes = True




###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  


class Members(Base):
    
    __tablename__ = "Members"

    member_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False, unique=False)
    last_name: Mapped[str] = mapped_column(nullable=False, unique=False)
    personal_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    role: Mapped[str] = mapped_column(nullable=False, unique=False)
    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)


class Member_Base(BaseModel):

    first_name: str
    last_name: str
    personal_number: str
    email: str
    role: str
    phone_number: str


class Member_Create(Member_Base):
    pass


class Member_Update(Member_Base):
    member_id: int


class Member_Response(Member_Base):

    member_id: int

    class Config:
        from_attributes = True



###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  


class Transactions(Base):

    __tablename__ = "Transactions"

    transaction_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    date: Mapped[str] = mapped_column(nullable=False, unique=False)  # Use `datetime` if preferred
    product_name: Mapped[str] = mapped_column(nullable=False, unique=False)
    brand_name: Mapped[str] = mapped_column(nullable=True, unique=False)
    price_sek: Mapped[float] = mapped_column(nullable=False, unique=False)
    units: Mapped[int] = mapped_column(nullable=True, unique=False)  # Nullable for kg-only transactions
    kg: Mapped[float] = mapped_column(nullable=True, unique=False)    # Nullable for unit-only transactions
    product_price: Mapped[float] = mapped_column(nullable=False, unique=False)
    store_name: Mapped[str] = mapped_column(nullable=True, unique=False)
    creditor: Mapped[str] = mapped_column(nullable=True, unique=False)

    

class Transaction_Base(BaseModel):

    date: str
    product_name: str
    brand_name: Optional[str] = None
    price_sek: float
    units: Optional[float] = None
    kg: Optional[float] = None
    product_price: float
    store_name: Optional[str] = None
    creditor: Optional[str] = None


class Transaction_Create(Transaction_Base):
    pass

    # @model_validator(mode="before")
    # def compute_product_price(cls, values):
    #     """Compute `product_price` based on `units`, `kg`, and `price_sek`."""
    #     price_sek = values.get("price_sek", 0)
    #     units = values.get("units")
    #     kg = values.get("kg")
        
    #     # Calculate product_price dynamically
    #     values["product_price"] = price_sek * (units if units is not None else (kg or 0))
    #     return values

class Transaction_Update(Transaction_Base):

    transaction_id: int


class Transaction_Response(Transaction_Base):

    transaction_id: int

    class Config:
        from_attributes = True

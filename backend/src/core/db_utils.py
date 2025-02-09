from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, sessionmaker, relationship
from sqlalchemy import create_engine, ForeignKey, inspect
from pydantic import BaseModel, model_validator
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Optional
import polars as pl


DB_PATH = r"C:\Users\Ale\Documents\code\pythonista\M10_server\m10_infra\backend\db\M10.db"#"../app/db/M10.db"
connection_url = f"sqlite:///{DB_PATH}"
engine = create_engine(connection_url, connect_args={"check_same_thread": False}, echo=False)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = session_local()
    try:
        yield db 

    finally:
        db.close()



def insert_table(df, table_name):

    df.write_database(
        table_name =table_name,
        connection = connection_url,
        if_table_exists = "append",
        engine="adbc"
                    )



def db_metadata():

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    tables_and_columns = {
        table: [column['name'] for column in inspector.get_columns(table)]
        for table in tables
    }

    print(tables_and_columns)
    return tables_and_columns



###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  

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



###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  



class Token(BaseModel):
    access_token: str
    token_type: str 


class Token_Data(BaseModel):
    username: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_base_user(base_user_data):
    """
    Creates a base user if it doesn't already exist in the User table.
    """

    # Hash the password
    base_user_data["hashed_password"] = pwd_context.hash(base_user_data["user_password"])

    # Start a database session
    with session_local() as db:
        # Check if the base user already exists
        base_user = db.query(User).filter(User.username == base_user_data["username"]).first()
        if not base_user:
            # If not, insert the base user
            new_user = User(
                username=base_user_data["username"],
                user_password=base_user_data["user_password"],
                hashed_password=base_user_data["hashed_password"],
                access_level=base_user_data["access_level"],
                disabled=base_user_data["disabled"],
            )
            db.add(new_user)
            db.commit()
            print("Base user created successfully.")
        else:
            print("Base user already exists.")



###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  


Base.metadata.create_all(bind=engine)


###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  



base_user_data = {
    "username": "admin",
    "user_password": "admin123",  # Plaintext password
    "access_level": 3,           # Highest access level (admin)
    "disabled": False
}

create_base_user(base_user_data)


base_user_data2 = {
    "username": "admin2",
    "user_password": "admin321",  # Plaintext password
    "access_level": 2,           # Highest access level (admin)
    "disabled": False
}

create_base_user(base_user_data2)


base_user_data1 = {
    "username": "admin1",
    "user_password": "admin321",  # Plaintext password
    "access_level": 1,           # Highest access level (admin)
    "disabled": False
}

create_base_user(base_user_data1)


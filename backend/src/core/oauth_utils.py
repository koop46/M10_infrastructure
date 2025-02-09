from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from core.db_utils import User_in_db, Token_Data, User, get_db
from dotenv import load_dotenv
import os 


load_dotenv()
secret_key = os.getenv("SECRET_KEY") 

SECRET_KEY = secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str, db, User_table = "Users"): #Get users

    user = db.query(User).filter(User.username == username).first()

    return user


def authenticate_user(username: str, password: str, db):

    user = get_user(username, db)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


async def get_current_user(token: str = Depends(oauth_2_scheme), db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        token_data = Token_Data(username=username)

    except JWTError:
        raise credentials_exception
    
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: User_in_db = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user


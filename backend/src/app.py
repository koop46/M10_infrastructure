from fastapi import FastAPI, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta
from routers.companies import router as company_router
from routers.contacts import router as contact_router
from routers.events import router as event_router
from routers.members import router as member_router
from routers.transactions import router as transaction_router
from routers.users import router as user_router
from core.oauth_utils import ACCESS_TOKEN_EXPIRE_MINUTES
from core.oauth_utils import create_access_token, timedelta, authenticate_user, get_current_active_user
from core.db_utils import Token, get_db, db_metadata, insert_table, engine, DB_PATH, User
import polars as pl


app = FastAPI()

@app.get("/")
def health_check():
    loser = {"M10 server": "Running"}
    return loser


app.include_router(company_router)
app.include_router(contact_router)
app.include_router(event_router)
app.include_router(member_router)
app.include_router(transaction_router)
app.include_router(user_router)



@app.get("/metadata")
def meta_data(current_user: User = Depends(get_current_active_user)):
    db_data = db_metadata()
    return db_data



# @app.post("/optional_query")
# def optional_query(request: Query, current_user: User = Depends(get_current_active_user)):

#     query = request.query

#     query_result = connector.fetch_data(query)

#     return query_result



@app.get("/download-db")
def download_db(current_user: User = Depends(get_current_active_user)):

    """
    Endpoint to download the SQLite database file.

    """


    return Response(content=open(DB_PATH, "rb").read(), media_type="application/octet-stream", headers={"Content-Disposition": "attachment; filename=M10.db"})



@app.post("/update_contacts/table")
def upload_contacts_csv(df_dict:dict, current_user: User = Depends(get_current_active_user)):

    try:
        df = pl.from_dict(df_dict)
        insert_table(df, "Contacts")
        print("Updated contacts table")

    except Exception as e:
        print(e)



@app.delete("/delete_table/{table_name}")
def delete_table(table_name: str, current_user: User = Depends(get_current_active_user)):
        
    with engine.connect() as connection:
        success = connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))

    if success:
        return {"message": f" {table_name} table deleted successfully."}
    
    else:
        return {"error": "Failed to delete participant."}
    

###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  ###  

@app.post("/token", response_model = Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):

    print("Form data", form_data.username, form_data.password)
    user = authenticate_user(form_data.username, form_data.password, db)
    print("gotten user: ", user.username)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}



from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token 
from sqlalchemy.orm import Session
from db import SessionLocal, init_db, Log
from schemas import LogCreate, LogResponse
from auth import verify_token
import db

app = FastAPI()

init_db()

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "testuser" or form_data.password != "testpassword":
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/logs", response_model=LogResponse)
def create_log(log: LogCreate, db: Session = Depends(get_db), token: str = Depends(verify_token)):
    db_log = Log(service_name=log.service_name, log_level=log.log_level, message=log.message)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@app.get("/logs")
def read_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logs = db.query(Log).offset(skip).limit(limit).all()
    return logs

from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        if not authorization.startswith("Bearer "):
            raise credentials_exception
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

@app.post("/messages", status_code=status.HTTP_201_CREATED)
def create_message(
    message: schemas.MessageCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_message = models.Message(
        user_id=current_user.id,
        message=message.message,
        time=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    
    return {}
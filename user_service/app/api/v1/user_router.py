from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.schemas import UserCreate, UserResponse
from app.api.v1.crud import create_user, get_user, get_users
from app.db.database import SessionLocal
from app.services.email_service import send_email
from app.utils.rabbitmq import send_message_to_rabbitmq

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register/", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    await send_email(user.email)
    send_message_to_rabbitmq(user.email)
    return db_user

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return get_users(db)

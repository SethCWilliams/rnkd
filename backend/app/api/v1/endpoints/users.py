from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.db.models import User as UserModel
from app.db.schemas import UserRead, UserCreate
import uuid

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    users = db.query(UserModel).all()
    return users

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserRead)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if email already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    db_user = UserModel(
        name=user_data.name,
        email=user_data.email,
        profile_image_url=user_data.profile_image_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user 
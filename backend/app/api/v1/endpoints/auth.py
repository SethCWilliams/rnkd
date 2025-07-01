from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.db.models import User as UserModel
from app.db.schemas import UserRead, UserCreate
from pydantic import BaseModel
from passlib.context import CryptContext

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    name: str
    email: str
    profile_image_url: str = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/register", response_model=UserRead)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if email already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    db_user = UserModel(
        name=user_data.name,
        email=user_data.email,
        profile_image_url=None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    # Find user by email
    user = db.query(UserModel).filter(UserModel.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # In a real implementation, you would verify the password hash
    # For now, we'll just check if the user exists
    # if not verify_password(user_credentials.password, user.password_hash):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # In real implementation, create JWT token
    return Token(
        access_token="dummy_jwt_token_123",
        token_type="bearer"
    )

@router.get("/me", response_model=UserRead)
async def get_current_user(db: Session = Depends(get_db)):
    """Get current user information"""
    # In real implementation, decode JWT token to get user_id
    # For now, return the first user
    user = db.query(UserModel).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    password: str
    name: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    email: str
    name: str
    profile_image_url: Optional[str] = None

# Dummy user data
DUMMY_USERS = {
    "user@example.com": {
        "id": 1,
        "email": "user@example.com",
        "password": "hashed_password_123",
        "name": "John Doe",
        "profile_image_url": None
    }
}

@router.post("/register", response_model=User)
async def register(user_data: UserRegister):
    """Register a new user"""
    if user_data.email in DUMMY_USERS:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # In real implementation, hash password and save to database
    new_user = {
        "id": len(DUMMY_USERS) + 1,
        "email": user_data.email,
        "password": "hashed_" + user_data.password,
        "name": user_data.name,
        "profile_image_url": None
    }
    DUMMY_USERS[user_data.email] = new_user
    
    return User(**{k: v for k, v in new_user.items() if k != "password"})

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Login user and return access token"""
    user = DUMMY_USERS.get(user_credentials.email)
    if not user or user["password"] != "hashed_" + user_credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # In real implementation, create JWT token
    return Token(
        access_token="dummy_jwt_token_123",
        token_type="bearer"
    )

@router.get("/me", response_model=User)
async def get_current_user():
    """Get current user information"""
    # In real implementation, decode JWT token
    user = DUMMY_USERS["user@example.com"]
    return User(**{k: v for k, v in user.items() if k != "password"}) 
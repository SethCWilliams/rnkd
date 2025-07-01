from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class UserProfile(BaseModel):
    id: int
    name: str
    email: str
    profile_image_url: Optional[str] = None

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    profile_image_url: Optional[str] = None

# Dummy user data
DUMMY_USERS = {
    1: {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "profile_image_url": None
    },
    2: {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane@example.com",
        "profile_image_url": "https://example.com/avatar.jpg"
    }
}

@router.get("/", response_model=List[UserProfile])
async def get_users():
    """Get all users"""
    return [UserProfile(**user) for user in DUMMY_USERS.values()]

@router.get("/{user_id}", response_model=UserProfile)
async def get_user(user_id: int):
    """Get user by ID"""
    user = DUMMY_USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(**user)

@router.put("/{user_id}", response_model=UserProfile)
async def update_user(user_id: int, user_update: UserProfileUpdate):
    """Update user profile"""
    user = DUMMY_USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user data
    if user_update.name is not None:
        user["name"] = user_update.name
    if user_update.profile_image_url is not None:
        user["profile_image_url"] = user_update.profile_image_url
    
    return UserProfile(**user) 
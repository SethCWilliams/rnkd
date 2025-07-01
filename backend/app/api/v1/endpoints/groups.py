from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.db.models import Group as GroupModel, User as UserModel, GroupUser as GroupUserModel
from app.db.schemas import GroupRead, GroupCreate, UserRead
import uuid

router = APIRouter()

@router.get("/", response_model=List[GroupRead])
async def get_groups(db: Session = Depends(get_db)):
    """Get all groups"""
    groups = db.query(GroupModel).all()
    return groups

@router.post("/", response_model=GroupRead)
async def create_group(group_data: GroupCreate, db: Session = Depends(get_db)):
    """Create a new group"""
    # Generate invite code if not provided
    invite_code = group_data.invite_code or str(uuid.uuid4())[:8].upper()
    
    # Create new group
    db_group = GroupModel(
        name=group_data.name,
        invite_code=invite_code
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get("/{group_id}", response_model=GroupRead)
async def get_group(group_id: int, db: Session = Depends(get_db)):
    """Get group by ID"""
    group = db.query(GroupModel).filter(GroupModel.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.get("/{group_id}/members", response_model=List[UserRead])
async def get_group_members(group_id: int, db: Session = Depends(get_db)):
    """Get group members"""
    # Check if group exists
    group = db.query(GroupModel).filter(GroupModel.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Get group members through the many-to-many relationship
    members = db.query(UserModel).join(GroupUserModel).filter(GroupUserModel.group_id == group_id).all()
    return members

@router.post("/{group_id}/join")
async def join_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    """Join a group using invite code"""
    # Check if group exists
    group = db.query(GroupModel).filter(GroupModel.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user is already in the group
    existing_membership = db.query(GroupUserModel).filter(
        GroupUserModel.group_id == group_id,
        GroupUserModel.user_id == user_id
    ).first()
    
    if existing_membership:
        raise HTTPException(status_code=400, detail="User is already a member of this group")
    
    # Add user to group
    group_user = GroupUserModel(group_id=group_id, user_id=user_id)
    db.add(group_user)
    db.commit()
    
    return {"message": "Successfully joined group"} 
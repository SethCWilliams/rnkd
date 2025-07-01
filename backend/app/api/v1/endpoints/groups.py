from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid

router = APIRouter()

class Group(BaseModel):
    id: int
    name: str
    invite_code: str
    created_by_user_id: int

class GroupCreate(BaseModel):
    name: str

class GroupMember(BaseModel):
    user_id: int
    name: str
    email: str

# Dummy group data
DUMMY_GROUPS = {
    1: {
        "id": 1,
        "name": "Movie Night Crew",
        "invite_code": "ABC123",
        "created_by_user_id": 1,
        "members": [1, 2]
    },
    2: {
        "id": 2,
        "name": "Book Club",
        "invite_code": "XYZ789",
        "created_by_user_id": 2,
        "members": [2]
    }
}

DUMMY_USERS = {
    1: {"id": 1, "name": "John Doe", "email": "john@example.com"},
    2: {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
}

@router.get("/", response_model=List[Group])
async def get_groups():
    """Get all groups"""
    return [Group(**{k: v for k, v in group.items() if k != "members"}) 
            for group in DUMMY_GROUPS.values()]

@router.post("/", response_model=Group)
async def create_group(group_data: GroupCreate):
    """Create a new group"""
    new_group = {
        "id": len(DUMMY_GROUPS) + 1,
        "name": group_data.name,
        "invite_code": str(uuid.uuid4())[:8].upper(),
        "created_by_user_id": 1,  # In real implementation, get from auth
        "members": [1]  # Creator is automatically a member
    }
    DUMMY_GROUPS[new_group["id"]] = new_group
    return Group(**{k: v for k, v in new_group.items() if k != "members"})

@router.get("/{group_id}", response_model=Group)
async def get_group(group_id: int):
    """Get group by ID"""
    group = DUMMY_GROUPS.get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return Group(**{k: v for k, v in group.items() if k != "members"})

@router.get("/{group_id}/members", response_model=List[GroupMember])
async def get_group_members(group_id: int):
    """Get group members"""
    group = DUMMY_GROUPS.get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    members = []
    for user_id in group["members"]:
        user = DUMMY_USERS.get(user_id)
        if user:
            members.append(GroupMember(**user))
    
    return members

@router.post("/join/{invite_code}")
async def join_group(invite_code: str):
    """Join group using invite code"""
    for group in DUMMY_GROUPS.values():
        if group["invite_code"] == invite_code:
            # In real implementation, add user to group members
            return {"message": f"Successfully joined {group['name']}", "group_id": group["id"]}
    
    raise HTTPException(status_code=404, detail="Invalid invite code") 
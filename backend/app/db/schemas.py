from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any
from enum import Enum

class ListTypeEnum(str, Enum):
    group = 'group'
    personal = 'personal'

class MediaTypeEnum(str, Enum):
    movie = 'movie'
    book = 'book'
    game = 'game'

class ListStatusEnum(str, Enum):
    open = 'open'
    voting = 'voting'
    closed = 'closed'

# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    profile_image_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True

# Group Schemas
class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    invite_code: Optional[str] = None

class GroupRead(GroupBase):
    id: int
    invite_code: str
    class Config:
        orm_mode = True

# GroupUser Schemas
class GroupUserBase(BaseModel):
    group_id: int
    user_id: int

class GroupUserCreate(GroupUserBase):
    pass

class GroupUserRead(GroupUserBase):
    id: int
    class Config:
        orm_mode = True

# MovieList Schemas
class MovieListBase(BaseModel):
    name: str
    type: ListTypeEnum
    media_type: MediaTypeEnum
    status: ListStatusEnum = ListStatusEnum.open
    group_id: Optional[int] = None

class MovieListCreate(MovieListBase):
    created_by_user_id: int

class MovieListRead(MovieListBase):
    id: int
    class Config:
        orm_mode = True

# MovieListItem Schemas
class MovieListItemBase(BaseModel):
    external_id: str
    title: str
    item_metadata: Optional[Any] = None
    movie_list_id: int

class MovieListItemCreate(MovieListItemBase):
    pass

class MovieListItemRead(MovieListItemBase):
    id: int
    class Config:
        orm_mode = True

# EloScore Schemas
class EloScoreBase(BaseModel):
    movie_list_id: int
    user_id: int
    movie_list_item_id: int
    score: float = 1200.0

class EloScoreCreate(EloScoreBase):
    pass

class EloScoreRead(EloScoreBase):
    id: int
    class Config:
        orm_mode = True

# Matchup Schemas
class MatchupBase(BaseModel):
    movie_list_id: int
    user_id: int
    item_a_id: int
    item_b_id: int
    winner_id: Optional[int] = None

class MatchupCreate(MatchupBase):
    pass

class MatchupRead(MatchupBase):
    id: int
    created_at: Optional[str]
    class Config:
        orm_mode = True 
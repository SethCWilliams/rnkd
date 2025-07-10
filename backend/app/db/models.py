from sqlalchemy import Column, Integer, String, ForeignKey, Enum, JSON, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class ListTypeEnum(str, enum.Enum):
    group = 'group'
    personal = 'personal'

class MediaTypeEnum(str, enum.Enum):
    movie = 'movie'
    book = 'book'
    game = 'game'

class ListStatusEnum(str, enum.Enum):
    open = 'open'
    voting = 'voting'
    closed = 'closed'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    profile_image_url = Column(String, nullable=True)
    groups = relationship('GroupUser', back_populates='user')

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    invite_code = Column(String, unique=True, nullable=False, index=True)
    users = relationship('GroupUser', back_populates='group')
    lists = relationship('MovieList', back_populates='group')

class GroupUser(Base):
    __tablename__ = 'group_users'
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    group = relationship('Group', back_populates='users')
    user = relationship('User', back_populates='groups')

class MovieList(Base):
    __tablename__ = 'movie_lists'
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)
    created_by_user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    type = Column(Enum(ListTypeEnum), nullable=False)
    media_type = Column(Enum(MediaTypeEnum), nullable=False)
    status = Column(Enum(ListStatusEnum), nullable=False, default=ListStatusEnum.open)
    group = relationship('Group', back_populates='lists')
    items = relationship('MovieListItem', back_populates='movie_list')

class MovieListItem(Base):
    __tablename__ = 'movie_list_items'
    id = Column(Integer, primary_key=True, index=True)
    movie_list_id = Column(Integer, ForeignKey('movie_lists.id'))
    external_id = Column(String, nullable=False)  # TMDB/ISBN/etc.
    title = Column(String, nullable=False)
    item_metadata = Column(JSON, nullable=True)
    movie_list = relationship('MovieList', back_populates='items')

class EloScore(Base):
    __tablename__ = 'elo_scores'
    id = Column(Integer, primary_key=True, index=True)
    movie_list_id = Column(Integer, ForeignKey('movie_lists.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_list_item_id = Column(Integer, ForeignKey('movie_list_items.id'))
    score = Column(Float, nullable=False, default=1200.0)

class Matchup(Base):
    __tablename__ = 'matchups'
    id = Column(Integer, primary_key=True, index=True)
    movie_list_id = Column(Integer, ForeignKey('movie_lists.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    item_a_id = Column(Integer, ForeignKey('movie_list_items.id'))
    item_b_id = Column(Integer, ForeignKey('movie_list_items.id'))
    winner_id = Column(Integer, ForeignKey('movie_list_items.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) 
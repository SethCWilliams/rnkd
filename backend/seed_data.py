#!/usr/bin/env python3
"""
Seed data script for Rnkd database
Run this to populate the database with initial test data
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.db.models import User, Group, GroupUser, MovieList, MovieListItem
from app.db.schemas import ListTypeEnum, MediaTypeEnum, ListStatusEnum

def seed_database():
    """Seed the database with initial test data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("Database already has data. Skipping seed.")
            return
        
        print("Seeding database with initial data...")
        
        # Create users
        users = [
            User(
                name="John Doe",
                email="john@example.com",
                profile_image_url=None
            ),
            User(
                name="Jane Smith", 
                email="jane@example.com",
                profile_image_url="https://example.com/avatar.jpg"
            ),
            User(
                name="Bob Wilson",
                email="bob@example.com", 
                profile_image_url=None
            )
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        
        # Refresh to get IDs
        for user in users:
            db.refresh(user)
        
        print(f"Created {len(users)} users")
        
        # Create groups
        groups = [
            Group(
                name="Movie Night Crew",
                invite_code="ABC123"
            ),
            Group(
                name="Book Club",
                invite_code="XYZ789"
            )
        ]
        
        for group in groups:
            db.add(group)
        db.commit()
        
        # Refresh to get IDs
        for group in groups:
            db.refresh(group)
        
        print(f"Created {len(groups)} groups")
        
        # Add users to groups
        group_memberships = [
            GroupUser(group_id=groups[0].id, user_id=users[0].id),  # John in Movie Night Crew
            GroupUser(group_id=groups[0].id, user_id=users[1].id),  # Jane in Movie Night Crew
            GroupUser(group_id=groups[1].id, user_id=users[1].id),  # Jane in Book Club
            GroupUser(group_id=groups[1].id, user_id=users[2].id),  # Bob in Book Club
        ]
        
        for membership in group_memberships:
            db.add(membership)
        db.commit()
        
        print(f"Created {len(group_memberships)} group memberships")
        
        # Create movie lists
        movie_lists = [
            MovieList(
                name="Classic Movies",
                group_id=groups[0].id,
                created_by_user_id=users[0].id,
                type=ListTypeEnum.group,
                media_type=MediaTypeEnum.movie,
                status=ListStatusEnum.open
            ),
            MovieList(
                name="My Watchlist",
                group_id=None,
                created_by_user_id=users[0].id,
                type=ListTypeEnum.personal,
                media_type=MediaTypeEnum.movie,
                status=ListStatusEnum.open
            ),
            MovieList(
                name="Sci-Fi Classics",
                group_id=groups[0].id,
                created_by_user_id=users[1].id,
                type=ListTypeEnum.group,
                media_type=MediaTypeEnum.movie,
                status=ListStatusEnum.voting
            )
        ]
        
        for movie_list in movie_lists:
            db.add(movie_list)
        db.commit()
        
        # Refresh to get IDs
        for movie_list in movie_lists:
            db.refresh(movie_list)
        
        print(f"Created {len(movie_lists)} movie lists")
        
        # Create movie list items
        movie_items = [
            # Classic Movies list
            MovieListItem(
                movie_list_id=movie_lists[0].id,
                external_id="278",
                title="The Shawshank Redemption",
                item_metadata={
                    "overview": "Two imprisoned men bond over a number of years...",
                    "poster_path": "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
                    "release_date": "1994-09-23",
                    "genre_ids": [18, 80]
                }
            ),
            MovieListItem(
                movie_list_id=movie_lists[0].id,
                external_id="238",
                title="The Godfather",
                item_metadata={
                    "overview": "Spanning the years 1945 to 1955...",
                    "poster_path": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
                    "release_date": "1972-03-14",
                    "genre_ids": [18, 80]
                }
            ),
            # My Watchlist
            MovieListItem(
                movie_list_id=movie_lists[1].id,
                external_id="680",
                title="Pulp Fiction",
                item_metadata={
                    "overview": "A burger-loving hit man...",
                    "poster_path": "/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
                    "release_date": "1994-09-10",
                    "genre_ids": [53, 80]
                }
            ),
            MovieListItem(
                movie_list_id=movie_lists[1].id,
                external_id="155",
                title="The Dark Knight",
                item_metadata={
                    "overview": "When the menace known as the Joker...",
                    "poster_path": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
                    "release_date": "2008-07-18",
                    "genre_ids": [28, 80, 18]
                }
            ),
            # Sci-Fi Classics (for voting)
            MovieListItem(
                movie_list_id=movie_lists[2].id,
                external_id="13",
                title="Forrest Gump",
                item_metadata={
                    "overview": "The presidencies of Kennedy and Johnson...",
                    "poster_path": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
                    "release_date": "1994-07-06",
                    "genre_ids": [35, 18]
                }
            ),
            MovieListItem(
                movie_list_id=movie_lists[2].id,
                external_id="550",
                title="Fight Club",
                item_metadata={
                    "overview": "A ticking-time-bomb insomniac...",
                    "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
                    "release_date": "1999-10-15",
                    "genre_ids": [18]
                }
            ),
            MovieListItem(
                movie_list_id=movie_lists[2].id,
                external_id="11",
                title="Star Wars",
                item_metadata={
                    "overview": "Princess Leia is captured and held hostage...",
                    "poster_path": "/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg",
                    "release_date": "1977-05-25",
                    "genre_ids": [12, 28, 878]
                }
            )
        ]
        
        for item in movie_items:
            db.add(item)
        db.commit()
        
        print(f"Created {len(movie_items)} movie list items")
        
        print("✅ Database seeded successfully!")
        print("\nTest data created:")
        print(f"- {len(users)} users")
        print(f"- {len(groups)} groups") 
        print(f"- {len(group_memberships)} group memberships")
        print(f"- {len(movie_lists)} movie lists")
        print(f"- {len(movie_items)} movie list items")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database() 
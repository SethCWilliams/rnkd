#!/usr/bin/env python3
"""
Create comprehensive test data for the Rnkd application.
This script populates the database with realistic test data for development and testing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.base import engine, SessionLocal
from app.db.models import (
    User, Group, GroupUser, MovieList, MovieListItem, 
    EloScore, Matchup, ListTypeEnum, MediaTypeEnum, ListStatusEnum
)
from passlib.context import CryptContext
import random
from datetime import datetime, timedelta

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_test_data():
    """Create comprehensive test data for the application"""
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(Matchup).delete()
        db.query(EloScore).delete()
        db.query(MovieListItem).delete()
        db.query(MovieList).delete()
        db.query(GroupUser).delete()
        db.query(Group).delete()
        db.query(User).delete()
        db.commit()
        
        # Create Users
        print("Creating users...")
        users = [
            User(
                name="John Doe",
                email="john@example.com",
                password_hash=get_password_hash("password123"),
                profile_image_url=None
            ),
            User(
                name="Jane Smith",
                email="jane@example.com",
                password_hash=get_password_hash("password123"),
                profile_image_url=None
            ),
            User(
                name="Bob Johnson",
                email="bob@example.com",
                password_hash=get_password_hash("password123"),
                profile_image_url=None
            ),
            User(
                name="Alice Brown",
                email="alice@example.com",
                password_hash=get_password_hash("password123"),
                profile_image_url=None
            ),
            User(
                name="Charlie Wilson",
                email="charlie@example.com",
                password_hash=get_password_hash("password123"),
                profile_image_url=None
            ),
            User(
                name="Diana Prince",
                email="diana@example.com",
                password_hash=get_password_hash("password123"),
                profile_image_url=None
            ),
        ]
        
        db.add_all(users)
        db.commit()
        
        # Create Groups
        print("Creating groups...")
        groups = [
            Group(
                name="Movie Night Crew",
                invite_code="MOVIE123"
            ),
            Group(
                name="Book Club",
                invite_code="BOOKS456"
            ),
            Group(
                name="Gaming Squad",
                invite_code="GAMES789"
            ),
            Group(
                name="Family Fun",
                invite_code="FAMILY99"
            ),
        ]
        
        db.add_all(groups)
        db.commit()
        
        # Create Group Memberships
        print("Creating group memberships...")
        group_users = [
            # Movie Night Crew (John, Jane, Bob, Alice)
            GroupUser(group_id=1, user_id=1),
            GroupUser(group_id=1, user_id=2),
            GroupUser(group_id=1, user_id=3),
            GroupUser(group_id=1, user_id=4),
            
            # Book Club (Jane, Alice, Charlie, Diana)
            GroupUser(group_id=2, user_id=2),
            GroupUser(group_id=2, user_id=4),
            GroupUser(group_id=2, user_id=5),
            GroupUser(group_id=2, user_id=6),
            
            # Gaming Squad (John, Bob, Charlie)
            GroupUser(group_id=3, user_id=1),
            GroupUser(group_id=3, user_id=3),
            GroupUser(group_id=3, user_id=5),
            
            # Family Fun (Alice, Diana)
            GroupUser(group_id=4, user_id=4),
            GroupUser(group_id=4, user_id=6),
        ]
        
        db.add_all(group_users)
        db.commit()
        
        # Create Movie Lists
        print("Creating movie lists...")
        movie_lists = [
            MovieList(
                name="Friday Night Movies",
                group_id=1,
                created_by_user_id=1,
                type=ListTypeEnum.group,
                media_type=MediaTypeEnum.movie,
                status=ListStatusEnum.voting
            ),
            MovieList(
                name="Classic Sci-Fi",
                group_id=1,
                created_by_user_id=2,
                type=ListTypeEnum.group,
                media_type=MediaTypeEnum.movie,
                status=ListStatusEnum.open
            ),
            MovieList(
                name="Summer Reading",
                group_id=2,
                created_by_user_id=4,
                type=ListTypeEnum.group,
                media_type=MediaTypeEnum.book,
                status=ListStatusEnum.closed
            ),
            MovieList(
                name="Co-op Games",
                group_id=3,
                created_by_user_id=1,
                type=ListTypeEnum.group,
                media_type=MediaTypeEnum.game,
                status=ListStatusEnum.open
            ),
            MovieList(
                name="John's Personal Watchlist",
                group_id=None,
                created_by_user_id=1,
                type=ListTypeEnum.personal,
                media_type=MediaTypeEnum.movie,
                status=ListStatusEnum.open
            ),
        ]
        
        db.add_all(movie_lists)
        db.commit()
        
        # Create Movie List Items
        print("Creating movie list items...")
        
        # Popular movies for Friday Night Movies
        friday_movies = [
            {"external_id": "278", "title": "The Shawshank Redemption", "metadata": {"year": 1994, "rating": 9.3}},
            {"external_id": "238", "title": "The Godfather", "metadata": {"year": 1972, "rating": 9.2}},
            {"external_id": "680", "title": "Pulp Fiction", "metadata": {"year": 1994, "rating": 8.9}},
            {"external_id": "155", "title": "The Dark Knight", "metadata": {"year": 2008, "rating": 9.0}},
            {"external_id": "550", "title": "Fight Club", "metadata": {"year": 1999, "rating": 8.8}},
            {"external_id": "13", "title": "Forrest Gump", "metadata": {"year": 1994, "rating": 8.8}},
            {"external_id": "769", "title": "GoodFellas", "metadata": {"year": 1990, "rating": 8.7}},
            {"external_id": "122", "title": "The Lord of the Rings: The Return of the King", "metadata": {"year": 2003, "rating": 8.9}},
        ]
        
        # Sci-Fi movies for Classic Sci-Fi
        scifi_movies = [
            {"external_id": "11", "title": "Star Wars", "metadata": {"year": 1977, "rating": 8.6}},
            {"external_id": "78", "title": "Blade Runner", "metadata": {"year": 1982, "rating": 8.1}},
            {"external_id": "603", "title": "The Matrix", "metadata": {"year": 1999, "rating": 8.7}},
            {"external_id": "1891", "title": "The Empire Strikes Back", "metadata": {"year": 1980, "rating": 8.7}},
            {"external_id": "185", "title": "A Clockwork Orange", "metadata": {"year": 1971, "rating": 8.3}},
            {"external_id": "62", "title": "2001: A Space Odyssey", "metadata": {"year": 1968, "rating": 8.3}},
        ]
        
        # Books for Summer Reading
        summer_books = [
            {"external_id": "isbn_9780553573404", "title": "A Game of Thrones", "metadata": {"author": "George R.R. Martin", "pages": 694}},
            {"external_id": "isbn_9780316769174", "title": "The Catcher in the Rye", "metadata": {"author": "J.D. Salinger", "pages": 277}},
            {"external_id": "isbn_9780141439518", "title": "Pride and Prejudice", "metadata": {"author": "Jane Austen", "pages": 279}},
            {"external_id": "isbn_9780544003415", "title": "The Lord of the Rings", "metadata": {"author": "J.R.R. Tolkien", "pages": 1216}},
            {"external_id": "isbn_9780385474542", "title": "The Handmaid's Tale", "metadata": {"author": "Margaret Atwood", "pages": 311}},
        ]
        
        # Games for Co-op Games
        coop_games = [
            {"external_id": "portal2", "title": "Portal 2", "metadata": {"platform": "PC", "genre": "Puzzle"}},
            {"external_id": "overcooked", "title": "Overcooked! 2", "metadata": {"platform": "Multi", "genre": "Party"}},
            {"external_id": "deep_rock", "title": "Deep Rock Galactic", "metadata": {"platform": "PC", "genre": "FPS"}},
            {"external_id": "stardew", "title": "Stardew Valley", "metadata": {"platform": "Multi", "genre": "Farming"}},
            {"external_id": "minecraft", "title": "Minecraft", "metadata": {"platform": "Multi", "genre": "Sandbox"}},
        ]
        
        # John's personal watchlist
        personal_movies = [
            {"external_id": "87", "title": "Indiana Jones: Raiders of the Lost Ark", "metadata": {"year": 1981, "rating": 8.5}},
            {"external_id": "105", "title": "Back to the Future", "metadata": {"year": 1985, "rating": 8.5}},
            {"external_id": "120", "title": "The Fellowship of the Ring", "metadata": {"year": 2001, "rating": 8.8}},
            {"external_id": "389", "title": "12 Angry Men", "metadata": {"year": 1957, "rating": 8.9}},
        ]
        
        # Create items for each list
        list_items = []
        
        # Friday Night Movies (list_id = 1)
        for item in friday_movies:
            list_items.append(MovieListItem(
                movie_list_id=1,
                external_id=item["external_id"],
                title=item["title"],
                item_metadata=item["metadata"]
            ))
        
        # Classic Sci-Fi (list_id = 2)
        for item in scifi_movies:
            list_items.append(MovieListItem(
                movie_list_id=2,
                external_id=item["external_id"],
                title=item["title"],
                item_metadata=item["metadata"]
            ))
        
        # Summer Reading (list_id = 3)
        for item in summer_books:
            list_items.append(MovieListItem(
                movie_list_id=3,
                external_id=item["external_id"],
                title=item["title"],
                item_metadata=item["metadata"]
            ))
        
        # Co-op Games (list_id = 4)
        for item in coop_games:
            list_items.append(MovieListItem(
                movie_list_id=4,
                external_id=item["external_id"],
                title=item["title"],
                item_metadata=item["metadata"]
            ))
        
        # John's Personal Watchlist (list_id = 5)
        for item in personal_movies:
            list_items.append(MovieListItem(
                movie_list_id=5,
                external_id=item["external_id"],
                title=item["title"],
                item_metadata=item["metadata"]
            ))
        
        db.add_all(list_items)
        db.commit()
        
        # Create ELO Scores (for the voting list)
        print("Creating ELO scores...")
        movie_list_items = db.query(MovieListItem).filter(MovieListItem.movie_list_id == 1).all()
        group_members = db.query(GroupUser).filter(GroupUser.group_id == 1).all()
        
        elo_scores = []
        for member in group_members:
            for item in movie_list_items:
                # Random ELO scores between 1000-1400 (realistic range)
                score = random.randint(1000, 1400)
                elo_scores.append(EloScore(
                    movie_list_id=1,
                    user_id=member.user_id,
                    movie_list_item_id=item.id,
                    score=score
                ))
        
        db.add_all(elo_scores)
        db.commit()
        
        # Create some matchups and votes
        print("Creating matchups...")
        matchups = []
        
        # Create some random matchups for the voting list
        for i in range(15):  # Create 15 matchups
            item_a = random.choice(movie_list_items)
            item_b = random.choice(movie_list_items)
            
            # Make sure we don't match an item with itself
            while item_a.id == item_b.id:
                item_b = random.choice(movie_list_items)
            
            user = random.choice(group_members)
            winner = random.choice([item_a, item_b]) if random.random() > 0.3 else None  # 70% chance of having a winner
            
            matchups.append(Matchup(
                movie_list_id=1,
                user_id=user.user_id,
                item_a_id=item_a.id,
                item_b_id=item_b.id,
                winner_id=winner.id if winner else None,
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 72))
            ))
        
        db.add_all(matchups)
        db.commit()
        
        print("✅ Test data created successfully!")
        print(f"Created:")
        print(f"  - {len(users)} users")
        print(f"  - {len(groups)} groups")
        print(f"  - {len(group_users)} group memberships")
        print(f"  - {len(movie_lists)} movie lists")
        print(f"  - {len(list_items)} list items")
        print(f"  - {len(elo_scores)} ELO scores")
        print(f"  - {len(matchups)} matchups")
        
        print("\n🔑 Test user credentials (all use password 'password123'):")
        for user in users:
            print(f"  - {user.email} ({user.name})")
            
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
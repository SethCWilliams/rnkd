from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.base import get_db
from app.db.models import MovieList as MovieListModel, MovieListItem as MovieListItemModel
from app.db.schemas import MovieListRead, MovieListCreate, MovieListItemRead, MovieListItemCreate
from pydantic import BaseModel

router = APIRouter()

class Movie(BaseModel):
    id: int
    title: str
    overview: str
    poster_path: Optional[str] = None
    release_date: str
    genre_ids: List[int]
    external_id: str  # TMDB ID

class MovieSearch(BaseModel):
    query: str

class MovieList(BaseModel):
    id: int
    name: str
    group_id: Optional[int]
    created_by_user_id: int
    type: str
    status: str

class MovieListItem(BaseModel):
    id: int
    movie_list_id: int
    external_id: str
    title: str
    metadata: Optional[dict] = None

# Dummy movie data for search (we'll keep this for now since we don't have TMDB integration yet)
DUMMY_MOVIES = [
    {
        "id": 1,
        "title": "The Shawshank Redemption",
        "overview": "Two imprisoned men bond over a number of years...",
        "poster_path": "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
        "release_date": "1994-09-23",
        "genre_ids": [18, 80],
        "external_id": "278"
    },
    {
        "id": 2,
        "title": "The Godfather",
        "overview": "Spanning the years 1945 to 1955...",
        "poster_path": "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
        "release_date": "1972-03-14",
        "genre_ids": [18, 80],
        "external_id": "238"
    },
    {
        "id": 3,
        "title": "Pulp Fiction",
        "overview": "A burger-loving hit man...",
        "poster_path": "/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
        "release_date": "1994-09-10",
        "genre_ids": [53, 80],
        "external_id": "680"
    },
    {
        "id": 4,
        "title": "The Dark Knight",
        "overview": "When the menace known as the Joker...",
        "poster_path": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "release_date": "2008-07-18",
        "genre_ids": [28, 80, 18],
        "external_id": "155"
    },
    {
        "id": 5,
        "title": "Fight Club",
        "overview": "A ticking-time-bomb insomniac...",
        "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
        "release_date": "1999-10-15",
        "genre_ids": [18],
        "external_id": "550"
    }
]

@router.get("/search", response_model=List[Movie])
async def search_movies(query: str = ""):
    """Search movies (dummy data for now)"""
    if not query:
        return DUMMY_MOVIES
    
    # Simple search by title
    results = [movie for movie in DUMMY_MOVIES if query.lower() in movie["title"].lower()]
    return results

@router.get("/popular", response_model=List[Movie])
async def get_popular_movies():
    """Get popular movies (dummy data for now)"""
    return DUMMY_MOVIES

@router.get("/{movie_id}", response_model=Movie)
async def get_movie(movie_id: int):
    """Get movie by ID (dummy data for now)"""
    movie = next((m for m in DUMMY_MOVIES if m["id"] == movie_id), None)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.get("/lists/", response_model=List[MovieListRead])
async def get_movie_lists(db: Session = Depends(get_db)):
    """Get all movie lists"""
    lists = db.query(MovieListModel).all()
    return lists

@router.post("/lists/", response_model=MovieListRead)
async def create_movie_list(list_data: MovieListCreate, db: Session = Depends(get_db)):
    """Create a new movie list"""
    db_list = MovieListModel(
        name=list_data.name,
        group_id=list_data.group_id,
        created_by_user_id=list_data.created_by_user_id,
        type=list_data.type,
        media_type=list_data.media_type,
        status=list_data.status
    )
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@router.get("/lists/{list_id}/items", response_model=List[MovieListItemRead])
async def get_movie_list_items(list_id: int, db: Session = Depends(get_db)):
    """Get items in a movie list"""
    # Check if list exists
    movie_list = db.query(MovieListModel).filter(MovieListModel.id == list_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="Movie list not found")
    
    items = db.query(MovieListItemModel).filter(MovieListItemModel.movie_list_id == list_id).all()
    return items

@router.post("/lists/{list_id}/items", response_model=MovieListItemRead)
async def add_movie_to_list(list_id: int, movie_data: MovieListItemCreate, db: Session = Depends(get_db)):
    """Add movie to list"""
    # Check if list exists
    movie_list = db.query(MovieListModel).filter(MovieListModel.id == list_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="Movie list not found")
    
    # Check if movie is already in the list
    existing_item = db.query(MovieListItemModel).filter(
        MovieListItemModel.movie_list_id == list_id,
        MovieListItemModel.external_id == movie_data.external_id
    ).first()
    
    if existing_item:
        raise HTTPException(status_code=400, detail="Movie is already in this list")
    
    # Add movie to list
    db_item = MovieListItemModel(
        movie_list_id=list_id,
        external_id=movie_data.external_id,
        title=movie_data.title,
        item_metadata=movie_data.item_metadata
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item 
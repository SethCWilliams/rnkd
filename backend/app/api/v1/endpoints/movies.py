from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

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
    group_id: Optional[int] = None
    created_by_user_id: int
    type: str  # "group" or "personal"
    status: str  # "open", "voting", "closed"

class MovieListItem(BaseModel):
    id: int
    movie_list_id: int
    external_id: str
    title: str
    metadata: dict

# Dummy movie data
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

# Dummy movie lists
DUMMY_MOVIE_LISTS = {
    1: {
        "id": 1,
        "name": "Classic Movies",
        "group_id": 1,
        "created_by_user_id": 1,
        "type": "group",
        "status": "open"
    },
    2: {
        "id": 2,
        "name": "My Watchlist",
        "group_id": None,
        "created_by_user_id": 1,
        "type": "personal",
        "status": "open"
    }
}

# Dummy movie list items
DUMMY_MOVIE_LIST_ITEMS = {
    1: [
        {"id": 1, "movie_list_id": 1, "external_id": "278", "title": "The Shawshank Redemption", "metadata": DUMMY_MOVIES[0]},
        {"id": 2, "movie_list_id": 1, "external_id": "238", "title": "The Godfather", "metadata": DUMMY_MOVIES[1]}
    ],
    2: [
        {"id": 3, "movie_list_id": 2, "external_id": "680", "title": "Pulp Fiction", "metadata": DUMMY_MOVIES[2]},
        {"id": 4, "movie_list_id": 2, "external_id": "155", "title": "The Dark Knight", "metadata": DUMMY_MOVIES[3]}
    ]
}

@router.get("/search", response_model=List[Movie])
async def search_movies(query: str = ""):
    """Search movies (dummy data)"""
    if not query:
        return DUMMY_MOVIES
    
    # Simple search by title
    results = [movie for movie in DUMMY_MOVIES if query.lower() in movie["title"].lower()]
    return results

@router.get("/popular", response_model=List[Movie])
async def get_popular_movies():
    """Get popular movies (dummy data)"""
    return DUMMY_MOVIES

@router.get("/{movie_id}", response_model=Movie)
async def get_movie(movie_id: int):
    """Get movie by ID"""
    movie = next((m for m in DUMMY_MOVIES if m["id"] == movie_id), None)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.get("/lists/", response_model=List[MovieList])
async def get_movie_lists():
    """Get all movie lists"""
    return [MovieList(**list_data) for list_data in DUMMY_MOVIE_LISTS.values()]

@router.post("/lists/", response_model=MovieList)
async def create_movie_list(list_data: dict):
    """Create a new movie list"""
    new_list = {
        "id": len(DUMMY_MOVIE_LISTS) + 1,
        "name": list_data.get("name", "New List"),
        "group_id": list_data.get("group_id"),
        "created_by_user_id": 1,  # In real implementation, get from auth
        "type": list_data.get("type", "personal"),
        "status": "open"
    }
    DUMMY_MOVIE_LISTS[new_list["id"]] = new_list
    DUMMY_MOVIE_LIST_ITEMS[new_list["id"]] = []
    return MovieList(**new_list)

@router.get("/lists/{list_id}/items", response_model=List[MovieListItem])
async def get_movie_list_items(list_id: int):
    """Get items in a movie list"""
    items = DUMMY_MOVIE_LIST_ITEMS.get(list_id, [])
    return [MovieListItem(**item) for item in items]

@router.post("/lists/{list_id}/items")
async def add_movie_to_list(list_id: int, movie_data: dict):
    """Add movie to list"""
    if list_id not in DUMMY_MOVIE_LIST_ITEMS:
        raise HTTPException(status_code=404, detail="Movie list not found")
    
    new_item = {
        "id": len(DUMMY_MOVIE_LIST_ITEMS[list_id]) + 1,
        "movie_list_id": list_id,
        "external_id": movie_data["external_id"],
        "title": movie_data["title"],
        "metadata": movie_data.get("metadata", {})
    }
    DUMMY_MOVIE_LIST_ITEMS[list_id].append(new_item)
    return MovieListItem(**new_item) 
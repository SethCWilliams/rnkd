from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import random

router = APIRouter()

class Matchup(BaseModel):
    id: int
    movie_list_id: int
    user_id: int
    item_a_id: int
    item_b_id: int
    winner_id: Optional[int] = None
    created_at: str

class Vote(BaseModel):
    matchup_id: int
    winner_id: int

class EloScore(BaseModel):
    id: int
    movie_list_id: int
    user_id: int
    movie_list_item_id: int
    score: float

# Dummy matchup data
DUMMY_MATCHUPS = {
    1: {
        "id": 1,
        "movie_list_id": 1,
        "user_id": 1,
        "item_a_id": 1,
        "item_b_id": 2,
        "winner_id": None,
        "created_at": "2024-01-01T10:00:00Z"
    },
    2: {
        "id": 2,
        "movie_list_id": 1,
        "user_id": 1,
        "item_a_id": 1,
        "item_b_id": 3,
        "winner_id": 1,
        "created_at": "2024-01-01T10:05:00Z"
    }
}

# Dummy Elo scores
DUMMY_ELO_SCORES = {
    1: {
        "id": 1,
        "movie_list_id": 1,
        "user_id": 1,
        "movie_list_item_id": 1,
        "score": 1200.0
    },
    2: {
        "id": 2,
        "movie_list_id": 1,
        "user_id": 1,
        "movie_list_item_id": 2,
        "score": 1200.0
    }
}

# Dummy movie list items for voting
DUMMY_MOVIE_ITEMS = {
    1: {"id": 1, "title": "The Shawshank Redemption", "external_id": "278"},
    2: {"id": 2, "title": "The Godfather", "external_id": "238"},
    3: {"id": 3, "title": "Pulp Fiction", "external_id": "680"},
    4: {"id": 4, "title": "The Dark Knight", "external_id": "155"}
}

@router.get("/matchups/{movie_list_id}", response_model=List[Matchup])
async def get_matchups(movie_list_id: int, user_id: int = 1):
    """Get matchups for a movie list and user"""
    matchups = [m for m in DUMMY_MATCHUPS.values() 
                if m["movie_list_id"] == movie_list_id and m["user_id"] == user_id]
    return [Matchup(**matchup) for matchup in matchups]

@router.post("/matchups/{movie_list_id}/generate")
async def generate_matchups(movie_list_id: int, user_id: int = 1):
    """Generate new matchups for voting"""
    # In real implementation, this would use Elo algorithm to generate optimal matchups
    # For now, just create random matchups
    items = [1, 2, 3, 4]  # Dummy item IDs
    
    new_matchups = []
    for i in range(len(items) - 1):
        for j in range(i + 1, len(items)):
            matchup_id = len(DUMMY_MATCHUPS) + 1
            matchup = {
                "id": matchup_id,
                "movie_list_id": movie_list_id,
                "user_id": user_id,
                "item_a_id": items[i],
                "item_b_id": items[j],
                "winner_id": None,
                "created_at": "2024-01-01T10:00:00Z"
            }
            DUMMY_MATCHUPS[matchup_id] = matchup
            new_matchups.append(matchup)
    
    return {"message": f"Generated {len(new_matchups)} matchups", "matchups": new_matchups}

@router.post("/vote")
async def submit_vote(vote: Vote):
    """Submit a vote for a matchup"""
    matchup = DUMMY_MATCHUPS.get(vote.matchup_id)
    if not matchup:
        raise HTTPException(status_code=404, detail="Matchup not found")
    
    if matchup["winner_id"] is not None:
        raise HTTPException(status_code=400, detail="Matchup already voted on")
    
    # Update matchup with winner
    matchup["winner_id"] = vote.winner_id
    
    # In real implementation, update Elo scores here
    # For now, just return success
    return {"message": "Vote submitted successfully", "matchup_id": vote.matchup_id}

@router.get("/scores/{movie_list_id}", response_model=List[EloScore])
async def get_elo_scores(movie_list_id: int, user_id: int = 1):
    """Get Elo scores for a movie list and user"""
    scores = [s for s in DUMMY_ELO_SCORES.values() 
              if s["movie_list_id"] == movie_list_id and s["user_id"] == user_id]
    return [EloScore(**score) for score in scores]

@router.get("/progress/{movie_list_id}")
async def get_voting_progress(movie_list_id: int, user_id: int = 1):
    """Get voting progress for a user"""
    matchups = [m for m in DUMMY_MATCHUPS.values() 
                if m["movie_list_id"] == movie_list_id and m["user_id"] == user_id]
    
    total_matchups = len(matchups)
    completed_matchups = len([m for m in matchups if m["winner_id"] is not None])
    
    return {
        "total_matchups": total_matchups,
        "completed_matchups": completed_matchups,
        "progress_percentage": (completed_matchups / total_matchups * 100) if total_matchups > 0 else 0
    }

@router.get("/next-matchup/{movie_list_id}")
async def get_next_matchup(movie_list_id: int, user_id: int = 1):
    """Get the next unvoted matchup"""
    matchups = [m for m in DUMMY_MATCHUPS.values() 
                if m["movie_list_id"] == movie_list_id and m["user_id"] == user_id and m["winner_id"] is None]
    
    if not matchups:
        return {"message": "No more matchups available"}
    
    # Return the first unvoted matchup
    matchup = matchups[0]
    item_a = DUMMY_MOVIE_ITEMS.get(matchup["item_a_id"])
    item_b = DUMMY_MOVIE_ITEMS.get(matchup["item_b_id"])
    
    return {
        "matchup": Matchup(**matchup),
        "item_a": item_a,
        "item_b": item_b
    } 
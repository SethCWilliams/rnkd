from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.base import get_db
from app.db.models import Matchup as MatchupModel, EloScore as EloScoreModel, MovieListItem as MovieListItemModel
from app.db.schemas import MatchupRead, MatchupCreate, EloScoreRead, EloScoreCreate
import random
from datetime import datetime

router = APIRouter()

@router.get("/matchups/{movie_list_id}", response_model=List[MatchupRead])
async def get_matchups(movie_list_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    """Get matchups for a movie list and user"""
    matchups = db.query(MatchupModel).filter(
        MatchupModel.movie_list_id == movie_list_id,
        MatchupModel.user_id == user_id
    ).all()
    return matchups

@router.post("/matchups/{movie_list_id}/generate")
async def generate_matchups(movie_list_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    """Generate new matchups for voting"""
    # Get all items in the movie list
    items = db.query(MovieListItemModel).filter(MovieListItemModel.movie_list_id == movie_list_id).all()
    
    if len(items) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 items to generate matchups")
    
    # Generate all possible pairs
    new_matchups = []
    for i in range(len(items) - 1):
        for j in range(i + 1, len(items)):
            # Check if matchup already exists
            existing_matchup = db.query(MatchupModel).filter(
                MatchupModel.movie_list_id == movie_list_id,
                MatchupModel.user_id == user_id,
                MatchupModel.item_a_id == items[i].id,
                MatchupModel.item_b_id == items[j].id
            ).first()
            
            if not existing_matchup:
                matchup = MatchupModel(
                    movie_list_id=movie_list_id,
                    user_id=user_id,
                    item_a_id=items[i].id,
                    item_b_id=items[j].id,
                    winner_id=None,
                    created_at=datetime.utcnow()
                )
                db.add(matchup)
                new_matchups.append(matchup)
    
    db.commit()
    
    return {"message": f"Generated {len(new_matchups)} new matchups", "matchups": new_matchups}

@router.post("/matchups/{matchup_id}/vote")
async def vote_on_matchup(matchup_id: int, winner_id: int, db: Session = Depends(get_db)):
    """Vote on a matchup"""
    matchup = db.query(MatchupModel).filter(MatchupModel.id == matchup_id).first()
    if not matchup:
        raise HTTPException(status_code=404, detail="Matchup not found")
    
    if matchup.winner_id is not None:
        raise HTTPException(status_code=400, detail="Matchup has already been voted on")
    
    # Validate winner_id is one of the items in the matchup
    if winner_id not in [matchup.item_a_id, matchup.item_b_id]:
        raise HTTPException(status_code=400, detail="Winner must be one of the items in the matchup")
    
    # Update matchup with winner
    matchup.winner_id = winner_id
    db.commit()
    
    # Update Elo scores (simplified for now)
    await update_elo_scores(matchup, winner_id, db)
    
    return {"message": "Vote recorded successfully"}

async def update_elo_scores(matchup: MatchupModel, winner_id: int, db: Session):
    """Update Elo scores after a vote (simplified implementation)"""
    # Get or create Elo scores for both items
    score_a = db.query(EloScoreModel).filter(
        EloScoreModel.movie_list_id == matchup.movie_list_id,
        EloScoreModel.user_id == matchup.user_id,
        EloScoreModel.movie_list_item_id == matchup.item_a_id
    ).first()
    
    score_b = db.query(EloScoreModel).filter(
        EloScoreModel.movie_list_id == matchup.movie_list_id,
        EloScoreModel.user_id == matchup.user_id,
        EloScoreModel.movie_list_item_id == matchup.item_b_id
    ).first()
    
    # Create scores if they don't exist
    if not score_a:
        score_a = EloScoreModel(
            movie_list_id=matchup.movie_list_id,
            user_id=matchup.user_id,
            movie_list_item_id=matchup.item_a_id,
            score=1200.0
        )
        db.add(score_a)
    
    if not score_b:
        score_b = EloScoreModel(
            movie_list_id=matchup.movie_list_id,
            user_id=matchup.user_id,
            movie_list_item_id=matchup.item_b_id,
            score=1200.0
        )
        db.add(score_b)
    
    # Simple Elo update (K=32)
    K = 32
    expected_a = 1 / (1 + 10**((score_b.score - score_a.score) / 400))
    expected_b = 1 - expected_a
    
    if winner_id == matchup.item_a_id:
        actual_a = 1
        actual_b = 0
    else:
        actual_a = 0
        actual_b = 1
    
    score_a.score += K * (actual_a - expected_a)
    score_b.score += K * (actual_b - expected_b)
    
    db.commit()

@router.get("/scores/{movie_list_id}", response_model=List[EloScoreRead])
async def get_elo_scores(movie_list_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    """Get Elo scores for a movie list and user"""
    scores = db.query(EloScoreModel).filter(
        EloScoreModel.movie_list_id == movie_list_id,
        EloScoreModel.user_id == user_id
    ).all()
    return scores

@router.get("/progress/{movie_list_id}")
async def get_voting_progress(movie_list_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    """Get voting progress for a user"""
    matchups = db.query(MatchupModel).filter(
        MatchupModel.movie_list_id == movie_list_id,
        MatchupModel.user_id == user_id
    ).all()
    
    total_matchups = len(matchups)
    completed_matchups = len([m for m in matchups if m.winner_id is not None])
    
    return {
        "total_matchups": total_matchups,
        "completed_matchups": completed_matchups,
        "progress_percentage": (completed_matchups / total_matchups * 100) if total_matchups > 0 else 0
    }

@router.get("/next-matchup/{movie_list_id}")
async def get_next_matchup(movie_list_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    """Get the next unvoted matchup"""
    matchup = db.query(MatchupModel).filter(
        MatchupModel.movie_list_id == movie_list_id,
        MatchupModel.user_id == user_id,
        MatchupModel.winner_id == None
    ).first()
    
    if not matchup:
        return {"message": "No more matchups available"}
    
    # Get the items for this matchup
    item_a = db.query(MovieListItemModel).filter(MovieListItemModel.id == matchup.item_a_id).first()
    item_b = db.query(MovieListItemModel).filter(MovieListItemModel.id == matchup.item_b_id).first()
    
    return {
        "matchup": matchup,
        "item_a": item_a,
        "item_b": item_b
    } 
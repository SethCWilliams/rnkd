from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, groups, movies, voting

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
api_router.include_router(voting.router, prefix="/voting", tags=["voting"]) 
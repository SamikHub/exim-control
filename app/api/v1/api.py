from fastapi import APIRouter
from app.api.v1.endpoints import example, user, group, auth

api_router = APIRouter()
api_router.include_router(example.router, prefix="/example", tags=["example"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(group.router, prefix="/groups", tags=["groups"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
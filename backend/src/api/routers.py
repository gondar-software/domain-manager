from fastapi import APIRouter
from src.api.endpoints import auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
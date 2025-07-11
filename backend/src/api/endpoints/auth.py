from fastapi import APIRouter, Depends, HTTPException
from src.dependencies import get_auth_service
from src.services import AuthService
from src.schemas import Auth, Token

auth_router = APIRouter()

@auth_router.post("/login", response_model=Token)
async def login(
    auth: Auth,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Endpoint to login and generate a token.
    """
    if not auth_service.validate_password(auth.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return auth_service.generate_token()
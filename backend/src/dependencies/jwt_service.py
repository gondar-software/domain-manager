from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from src.schemas import oauth2_scheme
from src.config import settings

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except (JWTError, ValueError) as e:
        raise credentials_exception
from src.schemas import Token
from src.config import settings
from .jwt_service import create_access_token

class AuthService:
    def __init__(self, password: str = settings.PASSWORD):
        self.password = password

    def validate_password(self, password: str) -> bool:
        return self.password == password

    def generate_token(self) -> Token:
        return create_access_token({})
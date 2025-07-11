from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GODADDY_API_KEY: str = "your_godaddy_api_key"
    GODADDY_API_SECRET: str = "your_godaddy_api_secret"
    DOMAIN: str = "your_domain.com"
    EMAIL_ADDRESS: str = "your_email@example.com"
    JWT_SECRET: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    TOKEN_EXPIRE_TIMEOUT: int = 120
    PASSWORD: str = "your_password"
    SERVER_PORT: int = 8001
    PROJECT_NAME: str = "Domain Manager"
    SECRET_KEY: str = "your_secret_key"

    class Config:
        env_file = ".env"

settings = Settings()
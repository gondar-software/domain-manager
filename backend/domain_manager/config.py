from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GODADDY_API_KEY: str = "your_godaddy_api_key"
    GODADDY_API_SECRET: str = "your_godaddy_api_secret"
    DOMAIN: str = "your_domain.com"
    EMAIL_ADDRESS: str = "your_email@example.com"

    class Config:
        env_file = ".env"

settings = Settings()
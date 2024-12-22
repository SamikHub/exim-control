from pydantic import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ADMIN_USERNAME: str  # Додайте цей рядок
    ADMIN_PASSWORD: str  # Додайте цей рядок

    class Config:
        env_file = ".env"

settings = Settings()
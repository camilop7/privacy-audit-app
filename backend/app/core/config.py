import os

class Settings:
    PROJECT_NAME: str = "Privacy Audit"
    DEBUG: bool = True

settings = Settings()

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")
ALGORITHM = "HS256"

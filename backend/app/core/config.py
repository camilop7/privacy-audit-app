from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Privacy Audit"
    DEBUG: bool = True
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    IPINFO_TOKEN: str = ""
    NUMVERIFY_API_KEY: str = ""
    REACT_APP_IPINFO_TOKEN: str = ""

    ENV: str = os.getenv("ENV", "local")
    DATABASE_URL: str = ""

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        if self.ENV == "docker":
            return "postgresql://postgres:yourpassword@db:5432/privacy_audit"
        return "postgresql://postgres:yourpassword@localhost:5432/privacy_audit"

    class Config:
        env_file = ".env"

settings = Settings()

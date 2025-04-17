from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Privacy Audit"
    DEBUG: bool = True
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    IPINFO_TOKEN: str  # used by backend

    # Pydantic doesn't raise errors
    NUMVERIFY_API_KEY: str = ""
    REACT_APP_IPINFO_TOKEN: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

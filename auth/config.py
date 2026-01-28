from pydantic_settings import BaseSettings, SettingsConfigDict

class AuthSettings(BaseSettings):
    # Security keys
    SECRET_KEY: str = "super-secret-default-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    TOKEN_URL: str = "/auth/login" #If you want to change the tokenUrl dynamically for different apps, add a field to AuthSettings in config.py:
    # Database URL - allows each app to point to its own DB
    DATABASE_URL: str = "sqlite:///./auth_database.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Initialize settings
auth_settings = AuthSettings()
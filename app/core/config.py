from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    SQLSERVER_SERVER: str
    SQLSERVER_DATABASE: str
    SQLSERVER_USERNAME: str
    SQLSERVER_PASSWORD: str
    
    # Security settings
    SECRET_KEY: str = "default-secret-key"
    
    # App settings
    DEBUG: bool = False
    API_PREFIX: str = "/api"
    ALLOW_ORIGIN: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()
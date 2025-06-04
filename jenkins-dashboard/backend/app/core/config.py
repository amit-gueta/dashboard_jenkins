from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Jenkins Dashboard Backend"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/jenkins_dashboard")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    JENKINS_URLS: list[str] = [url.strip() for url in os.getenv("JENKINS_URLS", "http://localhost:8080").split(',')]
    JENKINS_USER: str | None = os.getenv("JENKINS_USER")
    JENKINS_TOKEN: str | None = os.getenv("JENKINS_TOKEN")
    POLLING_INTERVAL_SECONDS: int = int(os.getenv("POLLING_INTERVAL_SECONDS", "120"))

    class Config:
        case_sensitive = True

settings = Settings()

from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Jenkins Dashboard Backend"
    # Ensure this DATABASE_URL matches the one in .env.example and docker-compose for the backend service
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://jenkins_user:jenkins_password@postgres_db:5432/jenkins_dashboard_db")
    API_V1_STR: str = "/api/v1"

    class Config:
        case_sensitive = True

settings = Settings()

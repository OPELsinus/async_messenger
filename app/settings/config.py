import os
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ADMIN_ID: str = os.getenv("ADMIN_ID")


settings = Settings()

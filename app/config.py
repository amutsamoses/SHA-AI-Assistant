# Configuration settings (API keys, environment variables)

import os
from dotenv import load_dotenv
from typing import Optional, Union

load_dotenv()

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)


class Config:
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    DEBUG: Optional[Union[str, bool]] = os.getenv("DEBUG")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    GOOGLE_GEMINI_API_KEY: str = os.getenv("GOOGLE_GEMINI_API_KEY")
    
    
    def __init__(self):
        # check for required environment variables
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is not set!")
        
        # attempt to convert debug to boolean
        if self.DEBUG is not None:
            self.DEBUG = self.DEBUG.lower() in ("true", "1", "yes")

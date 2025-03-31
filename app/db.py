# Database configuration for logging chat history

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# # postgresql database credentials
# user = "postgres"
# password = "12345"
# host = "localhost"
# port = "5432"
# database = "SHA_DB"

# DATABASE_URL="postgresql://postgres:12345@localhost:5432/SHA_DB"


# Explicitly specify the .env file location
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)


DATABASE_URL = os.getenv("DATABASE_URL")

# check if DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set, CHeck env file")


try:
    # create a database engine
    engine = create_engine(DATABASE_URL)
except SQLAlchemyError as e:
    raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

# Create a new session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create the base class for the ORM
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(engine, checkfirst=True)
    



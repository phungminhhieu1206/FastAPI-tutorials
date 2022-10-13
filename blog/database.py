from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# Connect to database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

# Create a session local for instance engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create model ORM for database
Base = declarative_base()

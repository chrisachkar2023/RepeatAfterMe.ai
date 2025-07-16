from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# set up database
DATABASE_URL = os.getenv("DATABASE_URL") # environmental var
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# users table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)

# words table
class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(Text, nullable=False)
    difficulty = Column(Text, nullable=False)

# create tables if they don't exist
Base.metadata.create_all(bind=engine)

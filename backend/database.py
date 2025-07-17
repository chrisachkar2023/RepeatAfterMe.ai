from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os

# set up postgres database
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
    
# saved words 
class SavedWord(Base):
    __tablename__ = "saved_words"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)

    user = relationship("User", backref="saved_words")
    word = relationship("Word")

    __table_args__ = (UniqueConstraint("user_id", "word_id", name="_user_word_uc"),)

# create tables if they don't exist
Base.metadata.create_all(bind=engine)

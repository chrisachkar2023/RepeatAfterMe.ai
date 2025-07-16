# this runs only once to create the words table

import csv
import os
from database import Base, Word, SessionLocal

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# make sure the tables exist
session = SessionLocal()
Base.metadata.create_all(bind=session.get_bind())

with open("backend/word_difficulty.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        word_text, difficulty = row[0], row[1]
        word_obj = Word(word=word_text, difficulty=difficulty.lower())
        session.add(word_obj)

session.commit()
session.close()

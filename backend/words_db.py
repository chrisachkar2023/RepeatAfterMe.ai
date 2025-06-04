import sqlite3

easy_words = [
    "cat", "bat", "ball", "Banana", "Apple", "Orange"
] 

medium_words = [
    "firetruck", "planet", "camera"
]

hard_words = [
    "architecture", "exemplary", "hypothesis"
]

connect = sqlite3.connect("words.db")
cursor = connect.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        difficulty TEXT NOT NULL
    )
""")

def insert_words_by_difficulty(list, difficulty):
    values = [(word, difficulty) for word in list]
    "INSERT INTO words (word, difficulty) VALUES (?, ?)"
    cursor.executemany(
        values   
    )

connect.commit()

cursor.execute("SELECT COUNT(*) FROM words")
count = cursor.fetchone()[0]

if count == 0:
    insert_words_by_difficulty(easy_words, "easy")
    insert_words_by_difficulty(medium_words, "medium")
    insert_words_by_difficulty(hard_words, "hard")
    connect.commit()

connect.close()
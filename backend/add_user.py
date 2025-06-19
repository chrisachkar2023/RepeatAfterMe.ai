import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def add_user(username, password):
    hashed_password = pwd_context.hash(password)
    
    conn = sqlite3.connect("backend/users.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, hashed_password)
    )
    
    conn.commit()
    conn.close()
    print(f"User '{username}' added successfully!")

if __name__ == "__main__":
    add_user("a", "b")

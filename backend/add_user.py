from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.database import SessionLocal, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def add_user(username: str, password: str) -> bool:
    hashed_password = pwd_context.hash(password)
    session: Session = SessionLocal()

    # Check if username already exists
    existing_user = session.query(User).filter(User.username == username).first()
    if existing_user:
        session.close()
        return False  # user exists

    # Add user
    new_user = User(username=username, password_hash=hashed_password)
    session.add(new_user)
    session.commit()
    session.close()
    return True
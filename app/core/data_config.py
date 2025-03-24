
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Define paths for specific files in the data folder
CHAT_HISTORY = os.path.join(DATA_DIR, "chat_history.json")
GROUPED_DATA = os.path.join(DATA_DIR, "grouped_data.json")
BOOKING_DATA = os.path.join(DATA_DIR, "updated_data.csv")


# database
DB_PATH = "data/test.db"
DB_URI = f'sqlite:///{DB_PATH}'

# app/core/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

load_dotenv()

DB_URl = os.getenv("DATABASE_URL")

engine = create_engine(url=DB_URl)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()
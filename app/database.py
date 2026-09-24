from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

DB_URl = settings.DATABASE_URL

engine = create_engine(url=DB_URl)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()

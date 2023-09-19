
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import user, password, database


# Replace with your own MySQL credentials
DATABASE_URL = f'mysql+pymysql://{user}:{password}@localhost:3306/{database}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(engine)

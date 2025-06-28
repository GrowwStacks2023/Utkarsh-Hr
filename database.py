# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import user, password, database

# Updated for Azure PostgreSQL
DATABASE_URL = f'postgresql://{user}:{password}@hr-growwstacks-server.postgres.database.azure.com:5432/{database}?sslmode=require'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(engine)
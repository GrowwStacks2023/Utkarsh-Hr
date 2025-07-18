# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

from config import user , password , database , host 


# Create SSL context (stronger, works on Windows too)
ssl_context = {
   "ssl_mode": "VERIFY_IDENTITY" ,
    
}
# Get database credentials from environment variables
# PostgreSQL connection URL
DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:3306/{database}'



print(f"🔗 Connecting to: mysql://{user}:***@{host}:5432/{database}")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False,
    connect_args={"ssl": ssl_context}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    try:
        Base.metadata.create_all(engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise e

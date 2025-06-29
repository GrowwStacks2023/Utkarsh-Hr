# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get database credentials from environment variables
user = os.getenv('DB_USER', 'xepkifivur')
password = os.getenv('DB_PASSWORD', 'qY0trr$8atp$RZVX')
database = os.getenv('DB_NAME', 'postgres')
host = os.getenv('DB_HOST', 'hr-growwstacks-server.postgres.database.azure.com')

# PostgreSQL connection URL
DATABASE_URL = f'postgresql://{user}:{password}@{host}:5432/{database}?sslmode=require'

print(f"🔗 Connecting to: postgresql://{user}:***@{host}:5432/{database}")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False
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
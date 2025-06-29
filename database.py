# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get database credentials from environment variables
user = os.getenv('DB_USER', 'mfexyzjecv')
password = os.getenv('DB_PASSWORD', 'Utkarsh@1234')
database = os.getenv('DB_NAME', 'gfydwceabn')
host = os.getenv('DB_HOST', 'hr-growwstacks-server.mysql.database.azure.com')

# ✅ MySQL Flexible Server connection string
DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:3306/{database}'

# ✅ Fixed print statement
print(f"🔗 Connecting to: mysql://{user}:***@{host}:3306/{database}")

# Create SQLAlchemy engine
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

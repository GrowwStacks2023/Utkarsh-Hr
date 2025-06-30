# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Azure-compatible SSL settings
ssl_args = {
    "ssl": {
        "ssl_ca": "/etc/ssl/certs/ca-certificates.crt"
    }
}

user = os.getenv('DB_USER', 'mfexyzjecv')
password = os.getenv('DB_PASSWORD', 'shubham_10')
host = os.getenv('DB_HOST', 'gfydwceabn.mysql.database.azure.com')
database = os.getenv('DB_NAME', 'hr-database')

DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:3306/{database}'

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=ssl_args  # 🟢 This is the fix
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

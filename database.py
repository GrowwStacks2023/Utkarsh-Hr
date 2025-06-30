from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get database credentials from environment variables (or use defaults for local dev)
user = os.getenv('DB_USER', 'mfexyzjecv')
password = os.getenv('DB_PASSWORD', 'shubham_10')
database = os.getenv('DB_NAME', 'hr-database')
host = os.getenv('DB_HOST', 'gfydwceabn.mysql.database.azure.com')

# Full MySQL URI with SSL CA path
DATABASE_URL = (
    f"mysql+pymysql://{user}:{password}@{host}:3306/{database}"
    f"?ssl_ca=/home/site/wwwroot/BaltimoreCyberTrustRoot.crt.pem"
)

print(f"🔗 Connecting to: mysql+pymysql://{user}:***@{host}:3306/{database}")

# SQLAlchemy Engine
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

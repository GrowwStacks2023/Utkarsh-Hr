# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from urllib.parse import quote_plus 


ca_cert_path = os.path.join(os.path.dirname(__file__), "BaltimoreCyberTrustRoot.crt.pem")
# Create SSL context (stronger, works on Windows too)
ssl_context = {
   "ssl_mode": "VERIFY_IDENTITY" ,
    
}

# Get database credentials from environment variables
user = os.getenv('DB_USER', 'mfexyzjecv')
password = os.getenv('DB_PASSWORD', 'Utkarsh@1234')
database = os.getenv('DB_NAME', 'hr-database')
host = os.getenv('DB_HOST', 'gfydwceabn.mysql.database.azure.com')


encoded_password = quote_plus(password)

DATABASE_URL = f'mysql+pymysql://{user}:{encoded_password}@{host}:3306/{database}'

# ✅ Fixed print statement
print(f"🔗 Connecting to: mysql://{user}:***@{host}:3306/{database}")


# Create SQLAlchemy engine
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

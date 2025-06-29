# db_initializer.py
from database import Base, engine
from models.user_model import User  # ✅ Import AFTER Base
from models.jobs_model import Job
from models.candidate_model import Candidate

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")

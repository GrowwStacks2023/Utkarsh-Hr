from database import Base, engine
from routers.Jobs.jobs_model import Job  # import all models here
from routers.User.user_model import User  # import all models here
from routers.Candidate.candidate_model import Candidate  # import all models here

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")

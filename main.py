# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys

# ✅ Import init_db function instead of engine, Base directly
try:
    from database import init_db  # Changed this line!
    from routers.User.user_controller import router as user_controller  
    from routers.Jobs.jobs_controller import router as jobs_controller
    from routers.Candidate.candidate_controller import router as candidate_controller
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

app = FastAPI(title="HR Growwstacks API", version="1.0.0")

# ✅ Create resumes directory safely
resumes_dir = os.path.join(os.getcwd(), "resumes")
try:
    os.makedirs(resumes_dir, exist_ok=True)
    app.mount("/resumes", StaticFiles(directory=resumes_dir), name="resumes")
    print("✅ Static files mounted successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not mount static files: {e}")

# ✅ REMOVED: Base.metadata.create_all(bind=engine) - this was causing the MySQL error!
# Database initialization moved to startup event below

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Add health check endpoints
@app.get("/")
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "HR Growwstacks API",
        "version": "1.0.0"
    }

# Routes
app.include_router(user_controller, prefix="/api", tags=["Users"])
app.include_router(jobs_controller, prefix="/api", tags=["Jobs"])
app.include_router(candidate_controller, prefix="/api", tags=["Candidates"])

# ✅ Move database initialization to startup event with error handling
@app.on_event("startup")
async def startup_event():
    print("🚀 HR Growwstacks API is starting up...")
    try:
        init_db()  # This calls the database initialization safely
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        # Let the app start anyway for debugging

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
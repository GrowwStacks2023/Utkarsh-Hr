# controllers/job_controller.py
from ast import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from routers.Jobs.jobs_model import Job, JobCreate, JobRead

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/jobs")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    try:
        print("Received job data:", job.dict())
        new_job = Job(**job.dict())
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return new_job
    except Exception as e:
        print("❌ Error creating job:", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/jobs/{job_id}")
def update_job(job_id: int, job: JobCreate, db: Session = Depends(get_db)):
    try:
        existing_job = db.query(Job).filter(Job.id == job_id).first()
        
        if not existing_job:
            raise HTTPException(status_code=404, detail="Job not found")

        for key, value in job.dict().items():
            setattr(existing_job, key, value)
        
        db.commit()
        db.refresh(existing_job)
        return existing_job

    except Exception as e:
        print("❌ Error updating job:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/jobinfo/{job_id}", response_model=JobRead)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    try:
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        return job

    except Exception as e:
        print("❌ Error fetching job:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

        

# 🔍 Get Jobs with Optional Status Filter
@router.get("/jobs", response_model=list[JobRead])
def list_jobs(status: str = None, db: Session = Depends(get_db)):
    query = db.query(Job)
    
    if status:
        query = query.filter(Job.status == 'published')
    
    jobs = query.all()
    return jobs



# 🔍 Get Jobs by CreatedBy with Optional Status Filter
@router.get("/jobs/{createdBy}", response_model=list[JobRead])
def listall_jobs(createdBy: int, status: str = None, db: Session = Depends(get_db)):
    query = db.query(Job).filter(Job.createdBy == createdBy)
    
    if status:
        query = query.filter(Job.status == 'published')

    jobs = query.all()
    return jobs


# 🔴 Delete Job by ID
@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"detail": "Job deleted successfully"}


# ✅ Update job status to "published"
@router.patch("/jobs/{job_id}/publish", response_model=JobRead)
def publish_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.status = "published"  # type: ignore
    db.commit()
    db.refresh(job)
    return job

# ✅ Update job status to "published"
@router.patch("/jobs/{job_id}/closed", response_model=JobRead)
def closed_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.status = "closed"  # type: ignore
    db.commit()
    db.refresh(job)
    return job

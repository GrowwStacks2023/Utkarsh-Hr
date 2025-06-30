# controllers/job_controller.py
from ast import List
import json
from fastapi import APIRouter, Body, Depends, UploadFile, File, Form, HTTPException
import httpx
from sqlalchemy.orm import Session
from database import SessionLocal
from routers.Jobs.jobs_model import Job, JobCreate, JobRead
import shutil
import os
from routers.Candidate.candidate_model import Candidate, CandidateRead
import openai
import pdfplumber
from config import base_url, op_api_key, G_email_from, G_smtp_username, G_smtp_password, op_api_project_id, vapi_key, vapi_assistant_id
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Set API Key directly (Not recommended — see note below)
openai.api_key = op_api_key
print("print api key", openai.api_key)
@router.post("/apply/{company_id}")
async def apply_job(
    company_id: str,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    qualification: str = Form(...),
    designation: str = Form(...),
    department: str = Form(...),
    job_id: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # ✅ Save resume file
        upload_dir = "resumes"
        os.makedirs(upload_dir, exist_ok=True)
        if not resume.filename:
            raise HTTPException(status_code=400, detail="No resume file uploaded")
        file_path = os.path.join(upload_dir, os.path.basename(resume.filename))

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        # ✅ Get job details
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job or not getattr(job, "description", None):
            raise HTTPException(status_code=404, detail="Job not found or missing description")

        job_description = job.description
        resumeScreenQualificationScore = job.resumeScreenQualificationScore

        # ✅ Extract resume text using pdfplumber
        def extract_text_from_pdf(path):
            with pdfplumber.open(path) as pdf:
                return "\n".join([page.extract_text() or "" for page in pdf.pages])

        resume_text = extract_text_from_pdf(file_path)

        # ✅ Build AI prompt
        prompt = f"""
You are an expert HR AI assistant specialized in matching candidate resumes with job descriptions.

Your task is to analyze the compatibility between a job posting and a candidate's resume, then provide a comprehensive scoring and decision.

## Job Description:
{job_description}

## Resume:
{resume_text}

## Instructions:
1. Score the candidate on Technical Skills, Experience, Soft Skills, and Bonus Qualifications.
2. Use scoring rules:
  - 90–100: Exceptional match
  - 80–89: Strong match
  - 70–79: Good match
  - 60–69: Fair match
  - Below 60: Poor match
3. Result:
  - If score >= {resumeScreenQualificationScore} → "SELECT CANDIDATE"
  - Else → "REJECT CANDIDATE"

## Output Format:
Respond ONLY in valid JSON. No markdown, no explanation.

Format:
{{
  "score": 0–100,
  "result": "SELECT CANDIDATE" or "REJECT CANDIDATE",
  "reason": "Brief justification for the decision"
}}

Respond in JSON format only.
"""

        print("print api key in call : ", openai.api_key)


        client = openai.OpenAI(
         api_key=op_api_key,         
         project=op_api_project_id         
        )

        # response = client.chat.completions.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "user", "content": "Hello!"}
        #     ]
        # )


        # ✅ OpenAI API call (use correct method)
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},  # JSON-enforced response
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # ✅ Extract response content
        content = response.choices[0].message.content if response.choices[0].message and response.choices[0].message.content else None
        if not content:
            raise HTTPException(status_code=500, detail="AI response did not contain any content.")
        try:
            analysis_json = json.loads(content)
        except Exception:
            raise HTTPException(status_code=500, detail="AI response was not valid JSON.")

        score = analysis_json.get("score")
        result = analysis_json.get("result")
        reason = analysis_json.get("reason")

        print(score)
        print(result)
        print(reason)

        # ✅ Save candidate in DB
        new_candidate = Candidate(
            name=name,
            email=email,
            phone=phone,
            qualification=qualification,
            designation=designation,
            department=department,
            resume_path=file_path,
            company_id=company_id,
            job_id=job_id,
            resume_screen_score=score,
            screening_result=result,
            screening_reason_result=reason,
            status="applied"
        )

        db.add(new_candidate)
        db.commit()
        db.refresh(new_candidate)

                # ✅ Send Email Based on Result
        if result == "SELECT CANDIDATE":
            send_selection_email(email=email, name=name)
            callvapi(phone=phone, email=email, name=name, candidate_id=new_candidate.id) # type: ignore
        else:
            send_rejection_email(email=email, name=name)


        return {
            "message": "Application submitted",
            "candidate": {
                "id": new_candidate.id,
                "name": new_candidate.name,
                "email": new_candidate.email,
                "score": score,
                "result": result,
                "reason": reason
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def callvapi(phone: str, email: str, name: str, candidate_id: int):
    try:
        # Format phone number to E.164
        candidate_phone = phone
        if not candidate_phone.startswith("+"):
            candidate_phone = "+91" + candidate_phone  # Adjust for your region

        vapi_payload = {
            "assistantId": vapi_assistant_id,
            "phoneNumberId": "9205066e-5106-472f-8f1e-c69f6bb419d9",
            "phoneNumber": {
                "twilioAccountSid": "AC447bed8973d2991b3d85cfb7b30922a8",
                "twilioPhoneNumber": "+1 (667) 297 7183"
            },
            "assistantOverrides": {
                "variableValues": {
                    "name": name,
                    "email": email,
                    "candidate_id": candidate_id
                }
            },
            "customer": {
                "number": candidate_phone
            }
        }

        vapi_headers = {
            "Authorization": f"Bearer {vapi_key}",
            "Content-Type": "application/json"
        }

        with httpx.Client() as client:
            vapi_response = client.post(
                "https://api.vapi.ai/call",  # ✅ Corrected endpoint
                headers=vapi_headers,
                json=vapi_payload
            )

        if vapi_response.status_code != 200:
            print(f"❌ Vapi call failed: {vapi_response.status_code}, {vapi_response.text}")
        else:
            print("✅ Vapi assistant triggered successfully!")

    except Exception as e:
        print(f"❌ Vapi API error: {e}")





# 🟡 Get All Candidates
@router.get("/candidates/{company_id}")
def list_all_candidates(company_id: int, db: Session = Depends(get_db)):
    # Join Candidate with Job and fetch necessary fields
    results = (
        db.query(
            Candidate,
            Job.title.label("job_title")
        )
        .join(Job, Candidate.job_id == Job.id, isouter=True)  # left outer join to include candidates without job
        .filter(Candidate.company_id == company_id)
        .all()
    )

    candidates = []
    for candidate, job_title in results:
        candidates.append({
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "qualification": candidate.qualification,
            "designation": candidate.designation,
            "department": candidate.department,
            "job_id": candidate.job_id,
            "resume_path": candidate.resume_path,
            "job_title": job_title,
            "created_at": candidate.created_at,
            "resume_screen_score": candidate.resume_screen_score,
            "screening_result": candidate.screening_result,
            "screening_reason_result": candidate.screening_reason_result,
            "status": candidate.status
        })

    return candidates



@router.get("/candidateinfo/{candidate_id}")
def get_candidate_info(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    resume_url = None
    if candidate.resume_path is not None:
        web_path = candidate.resume_path.replace("\\", "/")  # convert backslashes to slashes
        resume_url = f"{base_url}/{web_path}"

    return {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "phone": candidate.phone,
        "resume_url": resume_url
    }


def send_selection_email(email: str, name: str):
    subject = "You're Selected for the Next Round!"
    body = f"""
    Hi {name},

    Congratulations! Based on our initial screening, you have been selected to move forward to the next round.

    Hr Assistant Will Contact You Soon. Please Wait for the Call.

    Good luck!
    """

    send_email(email, subject, body)

def send_rejection_email(email: str, name: str):
    subject = "Application Update - Thank You for Applying"
    body = f"""
    Hi {name},

    Thank you for applying. After careful consideration, we regret to inform you that your application was not selected at this time.

    We wish you the best in your job search and future endeavors.

    Regards,
    HR Team
    """

    send_email(email, subject, body)

def send_email(to_email: str, subject: str, body: str):
    from_email = G_email_from
    from_password = G_smtp_password
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    msg = MIMEMultipart()
    msg["From"] = from_email or ""
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        if from_email and from_password:
            server.login(from_email, from_password)
            server.send_message(msg)
        else:
            raise ValueError("Email credentials are not properly configured")

@router.put("/candidates/update-screening/{candidate_id}")
def update_screening(
    candidate_id: int,
    hr_assistant_screen_score: int = Body(...),
    hr_assistant_result: str = Body(...),
    hr_assistant_reason_result: str = Body(...),
    hr_assistant_transcript: str = Body(...),
    db: Session = Depends(get_db)
):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate.hr_assistant_screen_score = hr_assistant_screen_score # type: ignore
    candidate.hr_assistant_result = hr_assistant_result # type: ignore
    candidate.hr_assistant_reason_result = hr_assistant_reason_result # type: ignore
    candidate.hr_assistant_transcript = hr_assistant_transcript # type: ignore

    db.commit()
    db.refresh(candidate)
    return candidate

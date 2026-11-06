from models import db
from models.jobs import Job
from models.candidates import Candidate
from models.interview_sessions import InterviewSession
from common.interviewer import InterviewManager

interview_manager = InterviewManager()


def get_invite_info_service(token: str):
    job = Job.query.filter_by(invite_token=token).first()
    if not job:
        return None, "Invalid or expired invitation link", 404

    if not job.is_active:
        return None, "This job application is no longer accepting submissions", 410

    return {
        "job": {
            "title": job.title,
            "level": job.level,
            "description": job.description,
            "company_name": job.company_name,
            "invite_token": job.invite_token,
        }
    }, None, 200


def register_candidate_service(token: str, dto):
    job = Job.query.filter_by(invite_token=token).first()
    if not job:
        return None, "Invalid or expired invitation link", 404

    if not job.is_active:
        return None, "Applications for this role are currently closed", 410

    resume_text = dto.resume_text
    # Parse resume if bytes provided and no text
    if not resume_text and dto.resume_bytes:
        print(f"Parsing resume for {dto.full_name} ({dto.resume_filename})...")
        parsed = interview_manager.parse_resume(dto.resume_bytes, dto.resume_filename)
        if parsed:
            resume_text = parsed

    # Create candidate
    candidate = Candidate(
        job_id=job.id,
        full_name=dto.full_name,
        email=dto.email,
        phone=dto.phone,
        resume_filename=dto.resume_filename,
        resume_text=resume_text,
        status="registered",
    )
    db.session.add(candidate)
    db.session.flush()

    # Create interview session
    session = InterviewSession(
        candidate_id=candidate.id,
        stage=0,
        status="pending",
        transcript=[],
    )
    db.session.add(session)
    db.session.commit()

    return {
        "message": "Candidate registered successfully. Ready to start interview.",
        "candidate_id": candidate.id,
        "session_token": session.session_token,
        "job": {
            "title": job.title,
            "level": job.level,
            "company_name": job.company_name,
        },
    }, None, 201


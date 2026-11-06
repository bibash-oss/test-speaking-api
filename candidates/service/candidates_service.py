from models import db
from models.candidates import Candidate
from models.jobs import Job
from models.organizations import Organization, UserRole
from models.interview_sessions import InterviewSession
from candidates.dto.candidates_dto import CandidateResponseDTO
from common.interviewer import InterviewManager

interview_manager = InterviewManager()


def get_candidate_service(candidate_id: str):
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return None
    return CandidateResponseDTO.format_candidate(candidate)


def register_direct_candidate_service(dto):
    """
    Allows a candidate to register directly from a candidate form.
    If a position or role is specified in the form, matches or creates a job for that position.
    If no position is specified, uses an active job or general interview session.
    """
    job = None

    # 1. Resolve explicit job_id if provided
    if getattr(dto, "job_id", None):
        job = Job.query.get(dto.job_id)

    # 2. If the candidate specified a position or role in the form:
    target_position = (getattr(dto, "position", "") or getattr(dto, "role", "")).strip()
    target_level = getattr(dto, "level", "").strip()
    if not target_level and target_position:
        t_low = target_position.lower()
        if "intern" in t_low:
            target_level = "Intern"
        elif "junior" in t_low:
            target_level = "Junior"
        elif "senior" in t_low:
            target_level = "Senior"
        elif "lead" in t_low:
            target_level = "Lead"
        else:
            target_level = ""

    if not job and target_position:
        job = Job.query.filter(Job.title.ilike(f"%{target_position}%")).first()
        if not job:
            org = Organization.query.first()
            if not org:
                from auth.service.auth_service import seed_default_organization
                org = seed_default_organization()
            if not org:
                org = Organization(
                    name="Ktmbees",
                    email="admin@ktmbees.com",
                    role=UserRole.ADMIN,
                    is_active=True,
                )
                org.set_password("!@ktm@#23int_erview")
                db.session.add(org)
                db.session.flush()

            job = Job(
                organization_id=org.id,
                title=target_position,
                level=target_level,
                description=f"Interview for the {target_position} position.",
                company_name="",
                is_active=True,
            )
            db.session.add(job)
            db.session.flush()

    # 3. Only if NO position or role was specified: use an active job or create a general interview
    if not job:
        job = Job.query.filter_by(is_active=True).first()

    if not job:
        job = Job.query.first()

    if not job:
        org = Organization.query.first()
        if not org:
            from auth.service.auth_service import seed_default_organization
            org = seed_default_organization()
        if not org:
            org = Organization(
                name="Ktmbees",
                email="admin@ktmbees.com",
                role=UserRole.ADMIN,
                is_active=True,
            )
            org.set_password("!@ktm@#23int_erview")
            db.session.add(org)
            db.session.flush()

        job = Job(
            organization_id=org.id,
            title="General Interview",
            level="",
            description="Interview session.",
            company_name="",
            is_active=True,
        )
        db.session.add(job)
        db.session.flush()

    resume_text = dto.resume_text
    if not resume_text and dto.resume_bytes:
        print(f"Parsing resume for {dto.full_name} ({dto.resume_filename})...")
        parsed = interview_manager.parse_resume(dto.resume_bytes, dto.resume_filename)
        if parsed:
            resume_text = parsed

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
        "session_id": session.session_token,
        "candidate": {
            "id": candidate.id,
            "full_name": candidate.full_name,
            "email": candidate.email,
            "phone": candidate.phone,
        },
        "job": {
            "id": job.id,
            "title": job.title,
            "level": job.level,
            "company_name": job.company_name,
        },
    }, None, 201


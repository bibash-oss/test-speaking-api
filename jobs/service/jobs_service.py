import os
from models import db
from models.jobs import Job


def create_job_service(dto, org_id: str = None, org_name: str = "Company"):
    company = dto.company_name or org_name
    job = Job(
        organization_id=org_id,
        title=dto.title,
        level=dto.level,
        description=dto.description,
        company_name=company,
    )
    db.session.add(job)
    db.session.commit()

    frontend_base = os.getenv("FRONTEND_URL", "http://localhost:3000")
    invite_url = f"{frontend_base}/invite/{job.invite_token}"

    res = job.to_dict()
    res["invite_url"] = invite_url
    return res


def list_jobs_service():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    frontend_base = os.getenv("FRONTEND_URL", "http://localhost:3000")

    result = []
    for j in jobs:
        d = j.to_dict()
        d["invite_url"] = f"{frontend_base}/invite/{j.invite_token}"
        result.append(d)

    return result


def get_job_service(job_id: str):
    job = Job.query.get(job_id)
    if not job:
        return None
    frontend_base = os.getenv("FRONTEND_URL", "http://localhost:3000")
    res = job.to_dict()
    res["invite_url"] = f"{frontend_base}/invite/{job.invite_token}"
    return res


def get_job_candidates_service(job_id: str):
    job = Job.query.get(job_id)
    if not job:
        return None

    candidates_list = []
    for c in job.candidates:
        c_dict = c.to_dict()
        session = c.interview_session
        if session:
            c_dict["interview"] = {
                "session_token": session.session_token,
                "status": session.status,
                "stage": session.stage,
                "scorecard": session.scorecard,
                "started_at": session.started_at.isoformat() if session.started_at else None,
                "completed_at": session.completed_at.isoformat() if session.completed_at else None,
            }
        else:
            c_dict["interview"] = None

        candidates_list.append(c_dict)

    return {
        "job": {
            "id": job.id,
            "title": job.title,
            "level": job.level,
            "company_name": job.company_name,
        },
        "candidate_count": len(candidates_list),
        "candidates": candidates_list,
    }


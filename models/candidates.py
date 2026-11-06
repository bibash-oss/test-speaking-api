import uuid
from datetime import datetime, timezone
from models import db


def generate_uuid():
    return str(uuid.uuid4())


class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    job_id = db.Column(
        db.String(36),
        db.ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    resume_filename = db.Column(db.String(255), nullable=True)
    resume_text = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default="registered", nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    interview_session = db.relationship(
        "InterviewSession",
        backref="candidate",
        uselist=False,
        lazy=True,
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "resume_filename": self.resume_filename,
            "has_resume": bool(self.resume_text),
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


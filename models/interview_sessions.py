import uuid
import secrets
from datetime import datetime, timezone
from models import db


def generate_uuid():
    return str(uuid.uuid4())


def generate_invite_token():
    return secrets.token_urlsafe(16)


class InterviewSession(db.Model):
    __tablename__ = "interview_sessions"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    candidate_id = db.Column(
        db.String(36),
        db.ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    session_token = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
        index=True,
        default=generate_invite_token,
    )
    stage = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(30), default="pending", nullable=False)
    transcript = db.Column(db.JSON, default=list, nullable=False)
    scorecard = db.Column(db.JSON, nullable=True)

    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "candidate_id": self.candidate_id,
            "session_token": self.session_token,
            "stage": self.stage,
            "status": self.status,
            "transcript": self.transcript or [],
            "scorecard": self.scorecard,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


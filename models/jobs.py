import uuid
import secrets
from datetime import datetime, timezone
from models import db


def generate_uuid():
    return str(uuid.uuid4())


def generate_invite_token():
    return secrets.token_urlsafe(16)


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    organization_id = db.Column(
        db.String(36),
        db.ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    title = db.Column(db.String(120), nullable=False)
    level = db.Column(db.String(50), nullable=False, default="Junior")
    description = db.Column(db.Text, nullable=False)
    company_name = db.Column(db.String(120), nullable=True, default="Company")
    invite_token = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
        index=True,
        default=generate_invite_token,
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    candidates = db.relationship("Candidate", backref="job", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "title": self.title,
            "level": self.level,
            "description": self.description,
            "company_name": self.company_name,
            "invite_token": self.invite_token,
            "is_active": self.is_active,
            "candidate_count": len(self.candidates) if self.candidates else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


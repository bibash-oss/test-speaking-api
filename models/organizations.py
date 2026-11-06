import uuid
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.enums.userEnum import UserRole


def generate_uuid():
    return str(uuid.uuid4())


class Organization(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum(UserRole, native_enum=False, length=50, values_callable=lambda obj: [e.value for e in obj]),
        default=UserRole.ADMIN,
        nullable=False,
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
    jobs = db.relationship("Job", backref="organization", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_super_admin(self) -> bool:
        current_role = self.role.value if hasattr(self.role, "value") else str(self.role)
        return current_role == UserRole.SUPER_ADMIN.value

    @property
    def is_admin(self) -> bool:
        current_role = self.role.value if hasattr(self.role, "value") else str(self.role)
        return current_role in (UserRole.ADMIN.value, UserRole.SUPER_ADMIN.value)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role.value if hasattr(self.role, "value") else str(self.role),
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


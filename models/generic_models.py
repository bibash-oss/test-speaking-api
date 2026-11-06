from datetime import datetime, timezone
from sqlalchemy.orm import declared_attr
from models import db


class GenericModel:
    """
    Generic model mixin providing standard audit and lifecycle fields:
    created_at, updated_at, created_by, updated_by, deleted_at.
    """

    @declared_attr
    def created_at(self):
        return db.Column(
            db.DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        )

    @declared_attr
    def updated_at(self):
        return db.Column(
            db.DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            nullable=False,
        )

    @declared_attr
    def created_by(self):
        return db.Column(db.String(36), nullable=True)

    @declared_attr
    def updated_by(self):
        return db.Column(db.String(36), nullable=True)

    @declared_attr
    def deleted_at(self):
        return db.Column(db.DateTime(timezone=True), nullable=True)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


# Alias TimestampMixin to match speaking-api convention as well
TimestampMixin = GenericModel


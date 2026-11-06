import uuid
from sqlalchemy.dialects.postgresql import JSONB
from models import db
from models.generic_models import GenericModel
from models.enums.questionEnum import QuestionType, QuestionDifficulty


def generate_uuid():
    return str(uuid.uuid4())


class Question(GenericModel, db.Model):
    __tablename__ = "questions"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(255), nullable=False)
    question_type = db.Column(
        db.Enum(QuestionType, native_enum=False, length=50, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        index=True,
    )
    difficulty = db.Column(
        db.Enum(QuestionDifficulty, native_enum=False, length=50, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=QuestionDifficulty.MEDIUM,
        index=True,
    )
    content = db.Column(JSONB().with_variant(db.JSON, "sqlite"), nullable=False, default=dict)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    duration = db.Column(db.Integer, nullable=True, default=120)  # duration in seconds

    def __init__(self, **kwargs):
        if "question_type" in kwargs and isinstance(kwargs["question_type"], str):
            kwargs["question_type"] = QuestionType.from_str(kwargs["question_type"])
        if "difficulty" in kwargs and isinstance(kwargs["difficulty"], str):
            kwargs["difficulty"] = QuestionDifficulty.from_str(kwargs["difficulty"])
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "question_type": self.question_type.value if hasattr(self.question_type, "value") else str(self.question_type),
            "difficulty": self.difficulty.value if hasattr(self.difficulty, "value") else str(self.difficulty),
            "content": self.content or {},
            "is_active": self.is_active,
            "duration": self.duration,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }


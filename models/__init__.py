# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models and generic mixins here so that Flask-Migrate and app see them
from .enums.userEnum import UserRole, RoleEnum
from .enums.questionEnum import QuestionType, QuestionDifficulty
from .generic_models import GenericModel, TimestampMixin
from .organizations import Organization
from .jobs import Job
from .candidates import Candidate
from .interview_sessions import InterviewSession
from .questions import Question

__all__ = [
    "db",
    "GenericModel",
    "TimestampMixin",
    "UserRole",
    "RoleEnum",
    "QuestionType",
    "QuestionDifficulty",
    "Organization",
    "Job",
    "Candidate",
    "InterviewSession",
    "Question",
]

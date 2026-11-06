import enum


class QuestionType(str, enum.Enum):
    ROLE_PLAY = "role_play"
    OET = "oet"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SITUATIONAL = "situational"
    PROBLEM_SOLVING = "problem_solving"
    SYSTEM_DESIGN = "system_design"
    CODING = "coding"
    INTRODUCTORY = "introductory"

    @classmethod
    def from_str(cls, val: str):
        if not val:
            return cls.TECHNICAL
        cleaned = str(val).strip().lower()
        for member in cls:
            if member.value == cleaned or member.name.lower() == cleaned:
                return member
        # Fallback to direct instantiation or member
        try:
            return cls(cleaned)
        except ValueError:
            return cls(val)


class QuestionDifficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    @classmethod
    def from_str(cls, val: str):
        if not val:
            return cls.MEDIUM
        cleaned = str(val).strip().lower()
        for member in cls:
            if member.value == cleaned or member.name.lower() == cleaned:
                return member
        try:
            return cls(cleaned)
        except ValueError:
            return cls(val)

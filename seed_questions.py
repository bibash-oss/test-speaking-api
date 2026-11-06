#!/usr/bin/env python3
"""
Seed script to insert or update the role play question in the database.

Usage:
    python seed_questions.py
    flask seed-questions
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from app import app
from models import db, Question, QuestionType, QuestionDifficulty


from seeds.oet_nursing_scenarios import OET_NURSING_SCENARIOS

CHEST_PAIN_SCENARIO = {
    "title": "Chest Pain and Patient Anxiety",
    "question_type": "ROLE_PLAY",
    "difficulty": "MEDIUM",
    "duration": 480,
    "is_active": True,
    "content": {
        "setting": "Local Medical Clinic",
        "timings": {
            "speaking_time": 300,
            "preparation_time": 180,
        },
        "candidate_card": {
            "role": "Nurse",
            "description": "You are a nurse working at a local medical clinic. You are consulting a 45-year-old patient who has been experiencing occasional chest pain for the past three days.",
            "tasks": [
                "Ask about the patient's symptoms, including the nature, location and duration of the chest pain.",
                "Ask about any associated symptoms.",
                "Explore relevant medical history and lifestyle factors.",
                "Acknowledge the patient's concerns and anxiety.",
                "Explain the importance of urgent medical assessment.",
                "Discuss appropriate investigations and the next steps.",
                "Check the patient's understanding and invite questions.",
            ],
        },
        "patient_card": {
            "description": "You are a 45-year-old patient who has been experiencing occasional chest pain for the past three days. You are worried that it may be a sign of a serious heart condition.",
            "tasks": [
                "Explain your symptoms to the nurse.",
                "Describe when the chest pain started and how it feels.",
                "Mention that the pain sometimes occurs during physical activity and improves with rest.",
                "Express your concern about having a heart attack.",
                "Ask whether your condition is serious.",
                "Ask whether you need to go to the hospital.",
                "Ask whether you should stop exercising.",
            ],
        },
    },
}

# 50 comprehensive OET Nursing roleplay scenarios + updated chest pain scenario
SEED_QUESTIONS = [CHEST_PAIN_SCENARIO] + [
    s for s in OET_NURSING_SCENARIOS if s["title"] != "Chest Pain and Patient Anxiety"
]


def seed_questions(items=None):
    """Seed questions into the database idempotently."""
    questions_to_seed = items or SEED_QUESTIONS
    seeded_records = []

    # Ensure tables exist
    try:
        db.create_all()
    except Exception as e:
        print(f"Notice during db.create_all: {e}")

    for item in questions_to_seed:
        title = item["title"]
        q_type = QuestionType.from_str(item.get("question_type", "role_play"))
        difficulty = QuestionDifficulty.from_str(item.get("difficulty", "medium"))

        existing = Question.query.filter_by(title=title).first()
        if existing:
            existing.question_type = q_type
            existing.difficulty = difficulty
            existing.content = item.get("content", {})
            existing.is_active = item.get("is_active", True)
            existing.duration = item.get("duration", 480)
            seeded_records.append(existing)
            print(f"🔄 Updated existing question: '{title}' (type: {existing.question_type.value}, difficulty: {existing.difficulty.value})")
        else:
            new_q = Question(
                title=title,
                question_type=q_type,
                difficulty=difficulty,
                content=item.get("content", {}),
                is_active=item.get("is_active", True),
                duration=item.get("duration", 480),
                created_by="system_seeder",
            )
            db.session.add(new_q)
            seeded_records.append(new_q)
            print(f"✅ Created new question: '{title}' (type: {new_q.question_type.value}, difficulty: {new_q.difficulty.value})")

    try:
        db.session.commit()
        print(f"🌱 Successfully committed {len(seeded_records)} question(s) to the database.")
        return seeded_records
    except Exception as e:
        db.session.rollback()
        print(f"❌ Failed to commit questions seed: {e}")
        return []


def main():
    with app.app_context():
        results = seed_questions()
        if not results:
            sys.exit(1)


if __name__ == "__main__":
    main()


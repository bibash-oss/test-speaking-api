import os
import unittest
from datetime import datetime, timezone

os.environ["DATABASE"] = "sqlite:///:memory:"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["GOOGLE_API_KEY"] = "mock_api_key_for_testing"

from app import app
from models import db, Question, QuestionType, QuestionDifficulty, GenericModel


class TestQuestionModel(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_generic_model_inheritance_and_fields(self):
        """Test Question model inherits GenericModel and contains all required fields."""
        self.assertTrue(issubclass(Question, GenericModel))

        with self.app.app_context():
            q = Question(
                title="Design a rate limiter",
                question_type=QuestionType.SYSTEM_DESIGN,
                difficulty=QuestionDifficulty.HARD,
                content={
                    "prompt": "How would you design a distributed rate limiter with Redis?",
                    "rubric": ["Token bucket vs sliding window", "Redis Lua script", "Race conditions"],
                },
                is_active=True,
                duration=300,
                created_by="admin_user_uuid",
                updated_by="admin_user_uuid",
            )
            db.session.add(q)
            db.session.commit()

            fetched = Question.query.filter_by(title="Design a rate limiter").first()
            self.assertIsNotNone(fetched)
            self.assertEqual(fetched.question_type, QuestionType.SYSTEM_DESIGN)
            self.assertEqual(fetched.difficulty, QuestionDifficulty.HARD)
            self.assertEqual(fetched.duration, 300)
            self.assertTrue(fetched.is_active)
            self.assertFalse(fetched.is_deleted)
            self.assertIsNone(fetched.deleted_at)
            self.assertIsNotNone(fetched.created_at)
            self.assertIsNotNone(fetched.updated_at)
            self.assertEqual(fetched.created_by, "admin_user_uuid")
            self.assertEqual(fetched.updated_by, "admin_user_uuid")

            # Test soft-delete flag
            fetched.deleted_at = datetime.now(timezone.utc)
            db.session.commit()
            self.assertTrue(fetched.is_deleted)

            # Test to_dict serialization
            data = fetched.to_dict()
            self.assertEqual(data["title"], "Design a rate limiter")
            self.assertEqual(data["question_type"], "system_design")
            self.assertEqual(data["difficulty"], "hard")
            self.assertIn("prompt", data["content"])
            self.assertIsNotNone(data["created_at"])
            self.assertIsNotNone(data["deleted_at"])

    def test_seed_role_play_question(self):
        """Test seeding the Chest Pain and Patient Anxiety role play question."""
        from seed_questions import seed_questions

        with self.app.app_context():
            records = seed_questions()
            self.assertGreaterEqual(len(records), 50)

            q = Question.query.filter_by(title="Chest Pain and Patient Anxiety").first()
            self.assertIsNotNone(q)
            self.assertEqual(q.question_type, QuestionType.ROLE_PLAY)
            self.assertEqual(q.difficulty, QuestionDifficulty.MEDIUM)
            self.assertEqual(q.duration, 480)
            self.assertTrue(q.is_active)

            # Check content structure matches official OET schema
            self.assertEqual(q.content["setting"], "Local Medical Clinic")
            self.assertEqual(q.content["candidate_card"]["role"], "Nurse")
            self.assertIn("tasks", q.content["candidate_card"])
            self.assertIn("description", q.content["candidate_card"])
            self.assertIn("tasks", q.content["patient_card"])
            self.assertIn("description", q.content["patient_card"])
            self.assertEqual(q.content["timings"]["preparation_time"], 180)
            self.assertEqual(q.content["timings"]["speaking_time"], 300)

            # Test idempotency (calling again updates without creating duplicate)
            records2 = seed_questions()
            self.assertGreaterEqual(len(records2), 50)
            count = Question.query.filter_by(title="Chest Pain and Patient Anxiety").count()
            self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()


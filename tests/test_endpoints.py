import os
import unittest
from unittest.mock import patch, MagicMock
import json

os.environ["DATABASE"] = "sqlite:///:memory:"
os.environ["GOOGLE_API_KEY"] = "mock_api_key_for_testing"

from app import app
from models import db
from models.organizations import Organization
from models.jobs import Job
from models.candidates import Candidate
from models.interview_sessions import InterviewSession
from models.enums.userEnum import UserRole
from common.auth import generate_token


class TestModularEndpoints(unittest.TestCase):
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

    def test_jobs_and_candidates_endpoints(self):
        with self.app.app_context():
            org = Organization(name="Ktmbees", email="org@ktmbees.com", role=UserRole.ADMIN)
            org.set_password("pass123")
            db.session.add(org)
            db.session.commit()
            token = generate_token(org)
            org_id = org.id

        headers = {"Authorization": f"Bearer {token}"}

        # 1. Create Job
        create_res = self.client.post("/api/jobs", json={
            "title": "Backend Engineer",
            "level": "Senior",
            "description": "Python, Flask, PostgreSQL",
            "company_name": "Ktmbees Tech",
        }, headers=headers)
        self.assertEqual(create_res.status_code, 201)
        job_data = create_res.get_json()["job"]
        job_id = job_data["id"]
        invite_token = job_data["invite_token"]
        self.assertEqual(job_data["title"], "Backend Engineer")

        # 2. List Jobs
        list_res = self.client.get("/api/jobs")
        self.assertEqual(list_res.status_code, 200)
        jobs_list = list_res.get_json()["jobs"]
        self.assertEqual(len(jobs_list), 1)

        # 3. Get Single Job
        get_res = self.client.get(f"/api/jobs/{job_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()["job"]["id"], job_id)

        # 4. Invite info endpoint
        invite_res = self.client.get(f"/api/invite/{invite_token}")
        self.assertEqual(invite_res.status_code, 200)
        self.assertIn("job", invite_res.get_json())

        # 5. Register candidate through invite
        reg_res = self.client.post(f"/api/invite/{invite_token}/register", json={
            "full_name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "9800000000",
            "resume_text": "Experienced senior developer",
        })
        self.assertEqual(reg_res.status_code, 201)
        reg_data = reg_res.get_json()
        cand_id = reg_data["candidate_id"]
        session_token = reg_data["session_token"]

        # 6. Get Job Candidates (Leaderboard)
        job_cands_res = self.client.get(f"/api/jobs/{job_id}/candidates", headers=headers)
        self.assertEqual(job_cands_res.status_code, 200)
        cands = job_cands_res.get_json()["candidates"]
        self.assertEqual(len(cands), 1)
        self.assertEqual(cands[0]["email"], "jane@example.com")

        # 7. Get Candidate Profile
        cand_profile_res = self.client.get(f"/api/candidates/{cand_id}", headers=headers)
        self.assertEqual(cand_profile_res.status_code, 200)
        cand_data = cand_profile_res.get_json()["candidate"]
        self.assertEqual(cand_data["full_name"], "Jane Doe")
        self.assertIsNotNone(cand_data.get("interview"))

        # 8. Register candidate directly WITHOUT invite link, role, or suggestions
        direct_res = self.client.post("/api/candidates/register", json={
            "full_name": "Direct Candidate",
            "email": "direct@example.com",
            "phone": "9812345678",
            "resume_text": "Experienced professional",
        })
        self.assertEqual(direct_res.status_code, 201)
        direct_data = direct_res.get_json()
        self.assertIn("session_token", direct_data)
        self.assertIn("candidate_id", direct_data)
        self.assertEqual(direct_data["candidate"]["full_name"], "Direct Candidate")
        self.assertEqual(direct_data["candidate"]["email"], "direct@example.com")

        # 9. Register candidate directly with specific position
        pos_res = self.client.post("/api/candidates/register", json={
            "full_name": "Nurse Candidate",
            "email": "nurse@example.com",
            "phone": "9812345679",
            "position": "Registered Nurse",
        })
        self.assertEqual(pos_res.status_code, 201)
        pos_data = pos_res.get_json()
        self.assertEqual(pos_data["job"]["title"], "Registered Nurse")

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_interview_blueprint_endpoints(self, mock_tts):
        mock_tts.return_value = ("mock_b64_audio", [])

        # Start interview
        start_res = self.client.post("/api/interview/start", json={
            "session_id": "test_modular_sess",
            "role": "Data Scientist",
            "level": "Junior",
            "total_stages": 3,
        })
        self.assertEqual(start_res.status_code, 200)
        data = start_res.get_json()
        self.assertEqual(data["session_id"], "test_modular_sess")
        self.assertEqual(data["stage"], 1)

        # Get session state
        state_res = self.client.get("/api/interview/state/test_modular_sess")
        self.assertEqual(state_res.status_code, 200)
        self.assertEqual(state_res.get_json()["stage"], 1)


if __name__ == "__main__":
    unittest.main()


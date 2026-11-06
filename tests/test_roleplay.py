import os
import unittest
import json
from unittest.mock import patch, MagicMock

os.environ["DATABASE"] = "sqlite:///:memory:"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["GOOGLE_API_KEY"] = "mock_api_key_for_testing"

from app import app, socketio
from models import db, Question, QuestionType, QuestionDifficulty
from common.roleplay_manager import RolePlayManager, RolePlayState
from roleplay.service.roleplay_service import roleplay_manager


class TestRolePlayFeature(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.socket_client = socketio.test_client(self.app)

        with self.app.app_context():
            db.create_all()
            # Seed our medical role play question
            q = Question(
                title="Chest Pain and Patient Anxiety",
                question_type=QuestionType.ROLE_PLAY,
                difficulty=QuestionDifficulty.MEDIUM,
                duration=480,
                content={
                    "scenario": {
                        "setting": "Local Medical Clinic",
                        "description": "Patient presenting with chest pain",
                    },
                    "candidate_card": {
                        "role": "Doctor",
                        "instructions": ["Explore chest pain", "Ask about family history", "Explain ECG"],
                    },
                    "patient_card": {
                        "role": "Patient",
                        "background_information": ["Pressure in chest for 3 days", "Worse walking up stairs"],
                        "medical_history": ["High blood pressure", "Father had heart attack"],
                        "concerns": ["Worried about heart attack"],
                        "personality": "Anxious and frightened",
                    },
                },
            )
            db.session.add(q)
            db.session.commit()
            self.question_id = q.id

        roleplay_manager.sessions.clear()
        roleplay_manager._session_locks.clear()

    def tearDown(self):
        if self.socket_client.is_connected():
            self.socket_client.disconnect()
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @patch("common.roleplay_manager.synthesize_speech_with_lipsync")
    def test_start_roleplay_patient_speaks_first(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [{"start": 0, "end": 100, "value": "A"}])

        session_id = "test_doc_session_1"
        res = roleplay_manager.start_roleplay(session_id=session_id, question_id=self.question_id)

        self.assertEqual(res["session_id"], session_id)
        self.assertEqual(res["role"], "patient")
        self.assertEqual(res["state"], RolePlayState.PATIENT_SPEAKING)
        self.assertEqual(res["emotional_state"], "anxious")
        self.assertIn("chest", res["text"].lower())
        self.assertEqual(res["audio"], "mock_audio_b64")

    @patch("common.roleplay_manager.synthesize_speech_with_lipsync")
    def test_doctor_speech_and_patient_response(self, mock_tts):
        mock_tts.return_value = ("mock_patient_reply_b64", [])

        session_id = "test_doc_session_2"
        roleplay_manager.start_roleplay(session_id=session_id, question_id=self.question_id)

        # Mock Gemini response to doctor
        mock_gemini_resp = MagicMock()
        mock_gemini_resp.text = json.dumps({
            "speech": "The pain is right in the middle of my chest, Doctor. It feels tight.",
            "emotional_state": "anxious",
            "concern_raised": "Is it a heart attack?",
            "is_complete": False,
        })

        with patch.object(roleplay_manager.client.models, "generate_content", return_value=mock_gemini_resp):
            reply = roleplay_manager.process_doctor_speech(
                session_id=session_id,
                doctor_text="Hello, could you tell me where you feel this pain?",
            )

            self.assertEqual(reply["role"], "patient")
            self.assertIn("middle of my chest", reply["text"])
            self.assertEqual(reply["emotional_state"], "anxious")
            self.assertEqual(reply["turn_count"], 2)

    @patch("common.roleplay_manager.synthesize_speech_with_lipsync")
    def test_evaluate_roleplay_scorecard(self, mock_tts):
        mock_tts.return_value = ("mock_farewell_b64", [])

        session_id = "test_doc_session_3"
        roleplay_manager.start_roleplay(session_id=session_id, question_id=self.question_id)

        # Simulate candidate consultation turn so candidate_turn_count > 0
        session = roleplay_manager.get_or_create_session(session_id)
        session["history"].append({
            "role": "doctor",
            "text": "Hello, I am Nurse Alex. Can you tell me more about your chest pain, when it began, and how severe it feels?",
            "timestamp": "2026-11-06T00:00:00Z"
        })
        session["turn_count"] = 2

        mock_eval_resp = MagicMock()
        mock_eval_resp.text = json.dumps({
            "overall_score": 8.8,
            "oet_grade": "A",
            "information_gathering_score": 9,
            "empathy_and_reassurance_score": 9,
            "explanation_clarity_score": 8,
            "checking_understanding_score": 9,
            "clinical_tasks_achieved": ["Explored chest pain location and duration"],
            "clinical_tasks_missed": [],
            "strengths": ["Excellent reassurance"],
            "areas_for_improvement": ["Keep practicing"],
            "summary": "Candidate demonstrated exemplary medical communication.",
        })

        with patch.object(roleplay_manager.client.models, "generate_content", return_value=mock_eval_resp):
            result = roleplay_manager.evaluate_roleplay(session_id=session_id)
            self.assertTrue(result["is_complete"])
            self.assertIsNotNone(result["scorecard"])
            self.assertEqual(result["scorecard"]["oet_grade"], "A")
            self.assertEqual(result["scorecard"]["overall_score"], 8.8)

    @patch("common.roleplay_manager.synthesize_speech_with_lipsync")
    def test_evaluate_abandoned_roleplay_zero_turns(self, mock_tts):
        mock_tts.return_value = ("mock_farewell_b64", [])

        session_id = "test_abandoned_session"
        roleplay_manager.start_roleplay(session_id=session_id, question_id=self.question_id)

        # Candidate did NOT speak (0 turns)
        result = roleplay_manager.evaluate_roleplay(session_id=session_id)
        self.assertTrue(result["is_complete"])
        scorecard = result["scorecard"]
        self.assertEqual(scorecard["oet_grade"], "E")
        self.assertEqual(scorecard["overall_score"], 1.0)
        self.assertEqual(scorecard["clinical_tasks_achieved"], [])
        self.assertGreater(len(scorecard["clinical_tasks_missed"]), 0)
        self.assertIn("prematurely", scorecard["summary"].lower())

    @patch("common.roleplay_manager.synthesize_speech_with_lipsync")
    def test_evaluate_fallback_when_gemini_fails(self, mock_tts):
        mock_tts.return_value = ("mock_farewell_b64", [])

        session_id = "test_fallback_session"
        roleplay_manager.start_roleplay(session_id=session_id, question_id=self.question_id)

        session = roleplay_manager.get_or_create_session(session_id)
        session["history"].append({
            "role": "doctor",
            "text": "Hello, I am Nurse Alex. Can you tell me more about your symptoms and when the chest pain began?",
            "timestamp": "2026-11-06T00:00:00Z"
        })
        session["history"].append({
            "role": "doctor",
            "text": "I see, let me examine you and run an electrocardiogram to check your heart.",
            "timestamp": "2026-11-06T00:01:00Z"
        })
        session["turn_count"] = 3

        # Simulate Gemini failing with an exception
        with patch.object(roleplay_manager.client.models, "generate_content", side_effect=Exception("API limit")):
            result = roleplay_manager.evaluate_roleplay(session_id=session_id)
            self.assertTrue(result["is_complete"])
            scorecard = result["scorecard"]
            # Brief 2-turn response falls back to realistic Grade E (2.0) rather than automatic Grade B
            self.assertEqual(scorecard["oet_grade"], "E")
            self.assertEqual(scorecard["overall_score"], 2.0)

    @patch("common.roleplay_manager.synthesize_speech_with_lipsync")
    def test_rest_endpoints(self, mock_tts):
        mock_tts.return_value = ("mock_audio", [])

        # 1. Start roleplay REST
        res = self.client.post("/api/roleplay/start", json={
            "session_id": "rest_test_sess",
            "question_id": self.question_id,
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["role"], "patient")

        # 2. Get state REST
        state_res = self.client.get("/api/roleplay/state/rest_test_sess")
        self.assertEqual(state_res.status_code, 200)
        self.assertEqual(state_res.get_json()["state"], "patient_speaking")

    @patch("common.roleplay_manager.synthesize_speech_with_lipsync")
    def test_socket_lifecycle(self, mock_tts):
        mock_tts.return_value = ("mock_audio", [])
        session_id = "socket_roleplay_sess"

        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.get_received()

        # Emit start_roleplay
        self.socket_client.emit("start_roleplay", {
            "session_id": session_id,
            "question_id": self.question_id,
        })
        received = self.socket_client.get_received()
        msg_events = [r for r in received if r["name"] == "patient_message"]
        state_events = [r for r in received if r["name"] == "roleplay_state"]

        self.assertTrue(len(msg_events) > 0)
        self.assertEqual(msg_events[0]["args"][0]["role"], "patient")
        self.assertTrue(len(state_events) > 0)

    @patch("common.roleplay_manager.synthesize_speech_with_lipsync")
    def test_start_oet_intro_and_consultation(self, mock_tts):
        mock_tts.return_value = ("mock_intro_audio", [])
        session_id = "test_oet_intro_session"

        # 1. Test Interlocutor Intro
        intro = roleplay_manager.start_oet_intro(session_id=session_id, question_id=self.question_id)
        self.assertEqual(intro["role"], "interlocutor")
        self.assertEqual(intro["phase"], "interlocutor_intro")
        self.assertEqual(intro["preparation_time"], 180)
        self.assertEqual(intro["speaking_time"], 300)
        self.assertIn("occupational english test", intro["text"].lower())
        self.assertIn("three minutes", intro["text"].lower())
        self.assertIn("preparation", intro["text"].lower())

        # 2. Test Consultation Transition
        consultation = roleplay_manager.start_consultation(session_id=session_id)
        self.assertEqual(consultation["role"], "patient")
        self.assertEqual(consultation["phase"], "roleplay")
        self.assertEqual(consultation["state"], RolePlayState.PATIENT_SPEAKING)
        self.assertIn("chest", consultation["text"].lower())

    @patch("common.roleplay_manager.synthesize_speech_with_lipsync")
    def test_rest_intro_and_consultation_endpoints(self, mock_tts):
        mock_tts.return_value = ("mock_audio", [])
        session_id = "test_rest_intro_sess"

        # Test POST /api/roleplay/intro
        resp_intro = self.client.post("/api/roleplay/intro", json={
            "session_id": session_id,
            "question_id": self.question_id,
        })
        self.assertEqual(resp_intro.status_code, 200)
        intro_data = resp_intro.get_json()
        self.assertEqual(intro_data["role"], "interlocutor")
        self.assertEqual(intro_data["preparation_time"], 180)

        # Test POST /api/roleplay/start-consultation
        resp_cons = self.client.post("/api/roleplay/start-consultation", json={
            "session_id": session_id,
        })
        self.assertEqual(resp_cons.status_code, 200)
        cons_data = resp_cons.get_json()
        self.assertEqual(cons_data["role"], "patient")
        self.assertIn("chest", cons_data["text"].lower())

    @patch("common.roleplay_manager.synthesize_speech_with_lipsync")
    def test_handover_after_preparation(self, mock_tts):
        mock_tts.return_value = ("mock_handover_audio", [])
        session_id = "test_handover_sess"

        # 1. Test Manager start_handover
        handover = roleplay_manager.start_handover(session_id=session_id, question_id=self.question_id)
        self.assertEqual(handover["role"], "interlocutor")
        self.assertEqual(handover["phase"], "handover")
        self.assertEqual(handover["state"], RolePlayState.DOCTOR_TURN)
        self.assertTrue(handover["doctor_starts"])
        self.assertIn("five minutes", handover["text"].lower())
        self.assertIn("stop you", handover["text"].lower())
        self.assertIn("start the role-play now", handover["text"].lower())

        # 2. Test REST POST /api/roleplay/handover
        resp_handover = self.client.post("/api/roleplay/handover", json={
            "session_id": session_id,
            "question_id": self.question_id,
        })
        self.assertEqual(resp_handover.status_code, 200)
        h_data = resp_handover.get_json()
        self.assertEqual(h_data["role"], "interlocutor")
        self.assertTrue(h_data["doctor_starts"])

        # 3. Test WebSocket preparation_completed event
        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.get_received()

        self.socket_client.emit("preparation_completed", {"session_id": session_id})
        received = self.socket_client.get_received()
        handover_events = [r for r in received if r["name"] == "roleplay_handover"]
        state_events = [r for r in received if r["name"] == "roleplay_state"]

        self.assertTrue(len(handover_events) > 0)
        self.assertEqual(handover_events[0]["args"][0]["doctor_starts"], True)
        self.assertTrue(len(state_events) > 0)
        self.assertEqual(state_events[0]["args"][0]["state"], "doctor_turn")

    @patch("common.roleplay_manager.synthesize_speech_with_lipsync")
    def test_finish_roleplay_and_time_up(self, mock_tts):
        mock_tts.return_value = ("mock_conclusion_audio", [{"start": 0, "end": 100, "value": "A"}])
        session_id = "test_finish_sess"

        # 1. Test Manager finish_roleplay
        finish_res = roleplay_manager.finish_roleplay(session_id=session_id)
        self.assertEqual(finish_res["role"], "interlocutor")
        self.assertEqual(finish_res["phase"], "finished")
        self.assertEqual(finish_res["state"], RolePlayState.COMPLETED)
        self.assertTrue(finish_res["is_complete"])
        self.assertEqual(finish_res["text"], "Thank you. That is the end of the role-play.")
        self.assertEqual(finish_res["conclusion_text"], "Thank you. That is the end of the role-play.")
        self.assertEqual(finish_res["audio"], "mock_conclusion_audio")

        # 2. Test REST POST /api/roleplay/finish
        resp_finish = self.client.post("/api/roleplay/finish", json={
            "session_id": session_id,
        })
        self.assertEqual(resp_finish.status_code, 200)
        f_data = resp_finish.get_json()
        self.assertEqual(f_data["role"], "interlocutor")
        self.assertEqual(f_data["text"], "Thank you. That is the end of the role-play.")
        self.assertTrue(f_data["is_complete"])

        # 3. Test WebSocket finish_roleplay event
        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.get_received()

        self.socket_client.emit("finish_roleplay", {"session_id": session_id})
        received = self.socket_client.get_received()
        finished_events = [r for r in received if r["name"] == "roleplay_finished"]
        conclusion_events = [r for r in received if r["name"] == "interlocutor_conclusion"]
        state_events = [r for r in received if r["name"] == "roleplay_state"]

        self.assertTrue(len(finished_events) > 0)
        self.assertEqual(finished_events[0]["args"][0]["role"], "interlocutor")
        self.assertEqual(finished_events[0]["args"][0]["text"], "Thank you. That is the end of the role-play.")
        self.assertTrue(finished_events[0]["args"][0]["is_complete"])

        self.assertTrue(len(conclusion_events) > 0)
        self.assertEqual(conclusion_events[0]["args"][0]["text"], "Thank you. That is the end of the role-play.")

        analyzing_events = [r for r in received if r["name"] == "analyzing"]
        self.assertTrue(len(analyzing_events) > 0)
        self.assertEqual(analyzing_events[0]["args"][0]["status"], "analyzing")

        self.assertTrue(len(state_events) > 0)
        self.assertEqual(state_events[0]["args"][0]["state"], "completed")
        self.assertEqual(state_events[0]["args"][0]["phase"], "finished")
        self.assertTrue(state_events[0]["args"][0]["is_complete"])

        # 4. Test WebSocket roleplay_time_up event
        time_up_sess = "test_time_up_sess"
        self.socket_client.emit("join", {"session_id": time_up_sess})
        self.socket_client.get_received()

        self.socket_client.emit("roleplay_time_up", {"session_id": time_up_sess})
        received_time_up = self.socket_client.get_received()
        time_up_finished = [r for r in received_time_up if r["name"] == "roleplay_finished"]
        self.assertTrue(len(time_up_finished) > 0)
        self.assertEqual(time_up_finished[0]["args"][0]["text"], "Thank you. That is the end of the role-play.")


if __name__ == "__main__":
    unittest.main()


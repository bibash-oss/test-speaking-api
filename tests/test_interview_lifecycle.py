import os
import json
import base64
import unittest
from unittest.mock import patch, MagicMock

# Ensure test DB or in-memory SQLite is used
os.environ["DATABASE"] = "sqlite:///:memory:"
os.environ["GOOGLE_API_KEY"] = "mock_api_key_for_testing"

from app import app, socketio, interview_manager
from common.interviewer import InterviewState


class TestInterviewLifecycle(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.socket_client = socketio.test_client(self.app)
        # Clear any existing in-memory sessions
        interview_manager.sessions.clear()
        interview_manager._session_locks.clear()

    def tearDown(self):
        if self.socket_client.is_connected():
            self.socket_client.disconnect()

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_connect_and_join(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [{"start": 0, "end": 100, "value": "A"}])
        received = self.socket_client.get_received()
        # Verify connection acknowledgement
        bot_msgs = [r for r in received if r["name"] == "bot_message"]
        self.assertTrue(len(bot_msgs) > 0)
        self.assertIn("Connected", bot_msgs[0]["args"][0]["message"])

        # Join room with a session
        self.socket_client.emit("join", {"session_id": "test_session_1"})
        received = self.socket_client.get_received()

        joined_events = [r for r in received if r["name"] == "joined"]
        state_events = [r for r in received if r["name"] == "interview_state"]

        self.assertEqual(len(joined_events), 1)
        self.assertEqual(joined_events[0]["args"][0]["session_id"], "test_session_1")
        self.assertEqual(joined_events[0]["args"][0]["state"], InterviewState.READY)

        self.assertEqual(len(state_events), 1)
        self.assertEqual(state_events[0]["args"][0]["state"], InterviewState.READY)

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_start_interview_success(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [{"start": 0, "end": 100, "value": "A"}])
        session_id = "test_session_start"

        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.get_received()

        # Start interview with total_stages = 3
        self.socket_client.emit("start_interview", {
            "session_id": session_id,
            "role": "Frontend Engineer",
            "level": "Mid",
            "total_stages": 3,
        })
        received = self.socket_client.get_received()

        state_events = [r for r in received if r["name"] == "interview_state"]
        msg_events = [r for r in received if r["name"] == "interviewer_message"]

        self.assertTrue(len(state_events) > 0)
        state_payload = state_events[0]["args"][0]
        self.assertEqual(state_payload["session_id"], session_id)
        self.assertEqual(state_payload["state"], InterviewState.INTERVIEWER_SPEAKING)
        self.assertEqual(state_payload["stage"], 1)
        self.assertEqual(state_payload["total_stages"], 3)
        self.assertEqual(state_payload["answered_stages"], 0)

        self.assertEqual(len(msg_events), 1)
        msg_payload = msg_events[0]["args"][0]
        self.assertEqual(msg_payload["session_id"], session_id)
        self.assertIn("Frontend Engineer", msg_payload["text"])
        self.assertEqual(msg_payload["audio"], "mock_audio_b64")
        self.assertFalse(msg_payload["is_complete"])

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_playback_finished_transitions_to_candidate_listening(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [])
        session_id = "test_session_turn"

        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.emit("start_interview", {"session_id": session_id, "total_stages": 3})
        self.socket_client.get_received()

        # Emit playback_finished
        self.socket_client.emit("playback_finished", {"session_id": session_id})
        received = self.socket_client.get_received()

        state_events = [r for r in received if r["name"] == "interview_state"]
        turn_events = [r for r in received if r["name"] == "candidate_turn"]

        self.assertEqual(len(state_events), 1)
        self.assertEqual(state_events[0]["args"][0]["state"], InterviewState.CANDIDATE_LISTENING)

        self.assertEqual(len(turn_events), 1)
        self.assertTrue(turn_events[0]["args"][0]["can_speak"])

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_candidate_text_answer_and_next_question(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [])
        session_id = "test_session_text"

        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.emit("start_interview", {"session_id": session_id, "total_stages": 3})
        self.socket_client.get_received()

        # Mock Gemini question generation
        mock_gemini_resp = MagicMock()
        mock_gemini_resp.text = json.dumps({
            "acknowledgement": "Great background.",
            "question": "Can you explain React useEffect dependencies?",
            "is_complete": False,
        })

        with patch.object(interview_manager.client.models, "generate_content", return_value=mock_gemini_resp):
            self.socket_client.emit("candidate_speech", {
                "session_id": session_id,
                "text": "I have 4 years of experience building React apps.",
            })

            received = self.socket_client.get_received()

            event_names = [r["name"] for r in received]
            self.assertIn("interview_state", event_names)
            self.assertIn("processing_status", event_names)
            self.assertIn("candidate_transcript", event_names)
            self.assertIn("interviewer_message", event_names)

            # Check next question
            msg_event = [r for r in received if r["name"] == "interviewer_message"][0]
            self.assertIn("React useEffect dependencies", msg_event["args"][0]["text"])
            self.assertEqual(msg_event["args"][0]["stage"], 2)

            # Check final state after question delivered
            final_state = [r for r in received if r["name"] == "interview_state"][-1]["args"][0]
            self.assertEqual(final_state["state"], InterviewState.INTERVIEWER_SPEAKING)
            self.assertEqual(final_state["stage"], 2)
            self.assertEqual(final_state["answered_stages"], 1)

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_candidate_audio_answer_with_transcription(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [])
        session_id = "test_session_audio"

        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.emit("start_interview", {"session_id": session_id, "total_stages": 3})
        self.socket_client.get_received()

        # Mock transcription & question generation
        mock_transcription_resp = MagicMock()
        mock_transcription_resp.text = "I specialize in TypeScript and Next.js."

        mock_question_resp = MagicMock()
        mock_question_resp.text = json.dumps({
            "acknowledgement": "Sounds good.",
            "question": "How do you handle SSR vs client components?",
            "is_complete": False,
        })

        # Return transcription on first call, question on second
        with patch.object(interview_manager.client.models, "generate_content", side_effect=[mock_transcription_resp, mock_question_resp]):
            fake_audio_b64 = base64.b64encode(b"RIFFdummywavbytes").decode("utf-8")
            self.socket_client.emit("candidate_speech", {
                "session_id": session_id,
                "audio": fake_audio_b64,
                "mime_type": "audio/wav",
            })

            received = self.socket_client.get_received()
            transcript_events = [r for r in received if r["name"] == "candidate_transcript"]
            self.assertEqual(len(transcript_events), 1)
            self.assertEqual(transcript_events[0]["args"][0]["text"], "I specialize in TypeScript and Next.js.")

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_full_lifecycle_to_interview_completed(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [])
        session_id = "test_session_complete"
        total_stages = 2

        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.emit("start_interview", {"session_id": session_id, "total_stages": total_stages})
        self.socket_client.get_received()

        # Answer 1 (stage 1 answered -> stage 2 question)
        mock_q2_resp = MagicMock()
        mock_q2_resp.text = json.dumps({
            "acknowledgement": "Understood.",
            "question": "What is your testing approach?",
            "is_complete": False,
        })

        with patch.object(interview_manager.client.models, "generate_content", return_value=mock_q2_resp):
            self.socket_client.emit("candidate_speech", {
                "session_id": session_id,
                "text": "Answer 1",
            })
            received = self.socket_client.get_received()
            self.assertFalse(any(r["name"] == "interview_completed" for r in received))

        # Answer 2 (stage 2 answered -> reaches total_stages -> interview completes!)
        mock_eval_resp = MagicMock()
        mock_eval_resp.text = json.dumps({
            "overall_score": 9.0,
            "recommendation": "Strong Hire",
            "technical_depth_score": 9,
            "communication_score": 9,
            "problem_solving_score": 9,
            "strengths": ["Excellent answers"],
            "concerns": [],
            "summary": "Candidate demonstrated strong skills across all domains.",
        })

        with patch.object(interview_manager.client.models, "generate_content", return_value=mock_eval_resp):
            self.socket_client.emit("candidate_speech", {
                "session_id": session_id,
                "text": "Answer 2: I write thorough unit tests with pytest.",
            })
            received = self.socket_client.get_received()

            completed_events = [r for r in received if r["name"] == "interview_completed"]
            self.assertEqual(len(completed_events), 1)
            comp_data = completed_events[0]["args"][0]
            self.assertEqual(comp_data["session_id"], session_id)
            self.assertEqual(comp_data["state"], "completed")
            self.assertEqual(comp_data["total_stages"], 2)
            self.assertEqual(comp_data["answered_stages"], 2)
            self.assertIn("completed", comp_data["message"].lower())
            self.assertIsNotNone(comp_data.get("scorecard"))
            self.assertEqual(comp_data["scorecard"]["recommendation"], "Strong Hire")

            final_state = [r for r in received if r["name"] == "interview_state"][-1]["args"][0]
            self.assertEqual(final_state["state"], InterviewState.COMPLETED)

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_reject_submission_after_completion(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [])
        session_id = "test_session_reject_complete"

        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.emit("start_interview", {"session_id": session_id, "total_stages": 1})
        self.socket_client.get_received()

        # Complete with 1 answer
        mock_eval = MagicMock()
        mock_eval.text = json.dumps({"overall_score": 8.0, "recommendation": "Hire", "summary": "Good."})
        with patch.object(interview_manager.client.models, "generate_content", return_value=mock_eval):
            self.socket_client.emit("candidate_speech", {"session_id": session_id, "text": "Only answer"})
            self.socket_client.get_received()

        # Attempt to submit another answer after completion
        self.socket_client.emit("candidate_speech", {"session_id": session_id, "text": "Post-completion answer"})
        received = self.socket_client.get_received()

        error_events = [r for r in received if r["name"] == "error"]
        self.assertEqual(len(error_events), 1)
        self.assertEqual(error_events[0]["args"][0]["code"], "SESSION_COMPLETED")

    def test_reject_concurrent_submission(self):
        session_id = "test_session_concurrent"
        session = interview_manager.get_or_create_session(session_id)
        session["is_processing"] = True  # simulate active processing

        self.socket_client.emit("candidate_speech", {"session_id": session_id, "text": "Concurrent answer"})
        received = self.socket_client.get_received()

        error_events = [r for r in received if r["name"] == "error"]
        self.assertEqual(len(error_events), 1)
        self.assertEqual(error_events[0]["args"][0]["code"], "CONCURRENT_PROCESSING")

    def test_missing_input_error(self):
        session_id = "test_session_missing"
        self.socket_client.emit("candidate_speech", {"session_id": session_id})
        received = self.socket_client.get_received()

        error_events = [r for r in received if r["name"] == "error"]
        self.assertEqual(len(error_events), 1)
        self.assertEqual(error_events[0]["args"][0]["code"], "MISSING_INPUT")

    def test_invalid_base64_audio_error(self):
        session_id = "test_session_invalid_b64"
        self.socket_client.emit("candidate_speech", {
            "session_id": session_id,
            "audio": "!!!not_valid_base64$$$",
        })
        received = self.socket_client.get_received()

        error_events = [r for r in received if r["name"] == "error"]
        self.assertEqual(len(error_events), 1)
        self.assertEqual(error_events[0]["args"][0]["code"], "INVALID_AUDIO")

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_reconnection_and_state_recovery(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [])
        session_id = "test_session_reconnect"

        # Start interview on client 1
        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.emit("start_interview", {"session_id": session_id, "total_stages": 4})
        self.socket_client.get_received()

        # Connect new client (simulating page reload)
        client2 = socketio.test_client(self.app)
        client2.emit("join", {"session_id": session_id})
        received = client2.get_received()

        state_events = [r for r in received if r["name"] == "interview_state"]
        msg_events = [r for r in received if r["name"] == "interviewer_message"]

        self.assertEqual(len(state_events), 1)
        self.assertEqual(state_events[0]["args"][0]["state"], InterviewState.INTERVIEWER_SPEAKING)
        self.assertEqual(state_events[0]["args"][0]["stage"], 1)

        # Verified that last message was delivered to reconnecting client
        self.assertEqual(len(msg_events), 1)
        self.assertEqual(msg_events[0]["args"][0]["stage"], 1)
        client2.disconnect()

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_idempotent_start_interview_on_active_session(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [])
        session_id = "test_session_idempotent"

        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.emit("start_interview", {"session_id": session_id, "total_stages": 5})
        self.socket_client.get_received()

        # Call start_interview again
        self.socket_client.emit("start_interview", {"session_id": session_id, "total_stages": 5})
        received = self.socket_client.get_received()

        state_events = [r for r in received if r["name"] == "interview_state"]
        msg_events = [r for r in received if r["name"] == "interviewer_message"]

        # Should recover current stage 1 without resetting or throwing errors
        self.assertEqual(state_events[0]["args"][0]["stage"], 1)
        self.assertEqual(msg_events[0]["args"][0]["stage"], 1)

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_gemini_failure_graceful_fallback(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [])
        session_id = "test_session_gemini_fallback"

        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.emit("start_interview", {"session_id": session_id, "total_stages": 3})
        self.socket_client.get_received()

        # Simulate Gemini throwing exception
        with patch.object(interview_manager.client.models, "generate_content", side_effect=Exception("API Rate Limit")):
            self.socket_client.emit("candidate_speech", {"session_id": session_id, "text": "My answer"})
            received = self.socket_client.get_received()

            msg_events = [r for r in received if r["name"] == "interviewer_message"]
            self.assertEqual(len(msg_events), 1)
            # Verifies fallback question was used rather than crashing
            self.assertIn("Could you tell me more about how you structure", msg_events[0]["args"][0]["text"])

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_tts_failure_graceful_fallback(self, mock_tts):
        # Simulate TTS returning None, None
        mock_tts.return_value = (None, None)
        session_id = "test_session_tts_fail"

        self.socket_client.emit("join", {"session_id": session_id})
        self.socket_client.emit("start_interview", {"session_id": session_id, "total_stages": 3})
        received = self.socket_client.get_received()

        msg_events = [r for r in received if r["name"] == "interviewer_message"]
        self.assertEqual(len(msg_events), 1)
        self.assertIsNone(msg_events[0]["args"][0]["audio"])
        self.assertIsNotNone(msg_events[0]["args"][0]["text"])

    @patch("common.interviewer.synthesize_speech_with_lipsync")
    def test_rest_api_start_and_respond(self, mock_tts):
        mock_tts.return_value = ("mock_audio_b64", [])
        http_client = self.app.test_client()

        # REST start
        resp = http_client.post("/api/interview/start", json={
            "session_id": "rest_test_session",
            "role": "Backend Engineer",
            "level": "Senior",
        })
        self.assertEqual(resp.status_code, 200)
        start_data = resp.get_json()
        self.assertEqual(start_data["session_id"], "rest_test_session")
        self.assertEqual(start_data["stage"], 1)
        self.assertEqual(start_data["state"], InterviewState.INTERVIEWER_SPEAKING)

        # REST respond
        mock_q = MagicMock()
        mock_q.text = json.dumps({"acknowledgement": "Good.", "question": "Next question?", "is_complete": False})
        with patch.object(interview_manager.client.models, "generate_content", return_value=mock_q):
            resp = http_client.post("/api/interview/respond", json={
                "session_id": "rest_test_session",
                "text": "Here is my backend architecture response.",
            })
            self.assertEqual(resp.status_code, 200)
            respond_data = resp.get_json()
            self.assertEqual(respond_data["stage"], 2)
            self.assertEqual(respond_data["state"], InterviewState.INTERVIEWER_SPEAKING)


if __name__ == "__main__":
    unittest.main()


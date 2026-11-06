import os
import json
import threading
from datetime import datetime, timezone
from dotenv import load_dotenv
from google import genai
from google.genai import types

from common.tts import synthesize_speech_with_lipsync
from models import db, Question, QuestionType, QuestionDifficulty, InterviewSession

load_dotenv()

DEFAULT_MODEL = "gemini-2.5-flash"


class RolePlayState:
    READY = "ready"
    INTERLOCUTOR_INTRO = "interlocutor_intro"
    PREPARATION = "preparation"
    HANDOVER = "handover"
    DOCTOR_TURN = "doctor_turn"
    PATIENT_SPEAKING = "patient_speaking"
    DOCTOR_LISTENING = "doctor_listening"
    PROCESSING_SPEECH = "processing_speech"
    COMPLETED = "completed"
    ERROR = "error"


class RolePlayManager:
    """
    Manages medical clinical consultation simulations where the AI plays the Patient
    and the Candidate/User acts as the Doctor.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.sessions = {}
        self._session_locks = {}
        self._meta_lock = threading.Lock()

    def _get_session_lock(self, session_id: str):
        with self._meta_lock:
            if session_id not in self._session_locks:
                self._session_locks[session_id] = threading.Lock()
            return self._session_locks[session_id]

    def _safe_db_query(self, query_fn):
        try:
            from flask import has_app_context
            if has_app_context():
                return query_fn()
        except Exception:
            pass

        try:
            from app import app
            with app.app_context():
                return query_fn()
        except Exception:
            return None

    def _get_db_session(self, session_id: str):
        return self._safe_db_query(
            lambda: InterviewSession.query.filter_by(session_token=session_id).first()
        )

    def _track_usage(self, session: dict, response) -> None:
        """Accumulate prompt and candidate token counts from Gemini responses."""
        if not session or not response:
            return
        usage = session.setdefault("usage", {
            "prompt_tokens": 0,
            "candidate_tokens": 0,
            "total_tokens": 0,
            "api_calls": 0,
        })
        try:
            meta = getattr(response, "usage_metadata", None)
            if meta:
                raw_p = getattr(meta, "prompt_token_count", 0)
                raw_c = getattr(meta, "candidates_token_count", 0)
                p_tokens = int(raw_p) if isinstance(raw_p, (int, float, str)) and str(raw_p).isdigit() else (raw_p if isinstance(raw_p, int) else 0)
                c_tokens = int(raw_c) if isinstance(raw_c, (int, float, str)) and str(raw_c).isdigit() else (raw_c if isinstance(raw_c, int) else 0)
                usage["prompt_tokens"] += p_tokens
                usage["candidate_tokens"] += c_tokens
                usage["total_tokens"] += (p_tokens + c_tokens)
                usage["api_calls"] += 1
        except Exception as e:
            print(f"Notice tracking Gemini usage: {e}")

    def _log_session_cost(self, session: dict) -> None:
        """
        Calculates and logs the total input/output tokens and cost
        for the completed OET session to the server console.
        """
        usage = session.get("usage", {})
        try:
            prompt_tokens = int(usage.get("prompt_tokens", 0) or 0)
        except (ValueError, TypeError):
            prompt_tokens = 0

        try:
            candidate_tokens = int(usage.get("candidate_tokens", 0) or 0)
        except (ValueError, TypeError):
            candidate_tokens = 0

        total_tokens = prompt_tokens + candidate_tokens
        try:
            api_calls = int(usage.get("api_calls", 0) or 0)
        except (ValueError, TypeError):
            api_calls = 0

        # Gemini 2.5 Flash Official Pricing:
        # Input (Prompt):     $0.30 per 1,000,000 tokens ($0.00000030 / token)
        # Output (Candidate): $2.50 per 1,000,000 tokens ($0.00000250 / token)
        input_cost = prompt_tokens * 0.00000030
        output_cost = candidate_tokens * 0.00000250
        total_cost = input_cost + output_cost

        session_id = session.get("session_id", "unknown")
        print("\n" + "=" * 68)
        print("📊 OET SESSION TOKEN USAGE & COST SUMMARY (Gemini)")
        print(f"Session ID: {session_id}")
        print(f"Total API Calls: {api_calls}")
        print("-" * 68)
        print(f"Input  (Prompt) Tokens:    {prompt_tokens:>8,d}  |  Cost: ${input_cost:.6f} USD")
        print(f"Output (Candidate) Tokens: {candidate_tokens:>8,d}  |  Cost: ${output_cost:.6f} USD")
        print(f"Total Tokens:              {total_tokens:>8,d}")
        print("-" * 68)
        print(f"💰 Total Estimated Gemini Cost: ${total_cost:.6f} USD")
        print("=" * 68 + "\n")

    def get_or_create_session(self, session_id: str, question_id: str = None, candidate_name: str = None) -> dict:
        if session_id not in self.sessions:
            question = None
            if question_id and str(question_id).lower() not in ["none", "null", "random", ""]:
                question = self._safe_db_query(lambda: Question.query.get(question_id))

            # Randomly select one active role-play question from DB if not specified
            if not question:
                question = self._safe_db_query(
                    lambda: Question.query.filter_by(
                        question_type=QuestionType.ROLE_PLAY,
                        is_active=True,
                    )
                    .order_by(db.func.random())
                    .first()
                )

            # Fallback to any role-play question if random query had an issue
            if not question:
                question = self._safe_db_query(
                    lambda: Question.query.filter_by(question_type=QuestionType.ROLE_PLAY).first()
                )

            q_data = question.to_dict() if question else {
                "title": "Chest Pain and Patient Anxiety",
                "question_type": "role_play",
                "difficulty": "medium",
                "duration": 480,
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

            # Ensure full backward and forward compatibility for frontend rendering
            content = q_data.setdefault("content", {})
            cand = content.setdefault("candidate_card", {})
            cand_tasks = cand.get("tasks") or cand.get("instructions", [])
            cand["tasks"] = cand_tasks
            cand["instructions"] = cand_tasks  # alias for legacy frontend code
            setting = content.get("setting") or content.get("scenario", {}).get("setting", "Local Medical Clinic")
            content["setting"] = setting
            content.setdefault("scenario", {"setting": setting, "description": cand.get("description", "")})

            self.sessions[session_id] = {
                "session_id": session_id,
                "question_id": question.id if question else "default_roleplay",
                "question": q_data,
                "history": [],
                "state": RolePlayState.READY,
                "turn_count": 0,
                "is_processing": False,
                "candidate_name": candidate_name or None,
                "started_at": None,
                "completed_at": None,
                "scorecard": None,
                "last_patient_message": None,
                "usage": {
                    "prompt_tokens": 0,
                    "candidate_tokens": 0,
                    "total_tokens": 0,
                    "api_calls": 0,
                },
            }

        if candidate_name and not self.sessions[session_id].get("candidate_name"):
            self.sessions[session_id]["candidate_name"] = candidate_name

        if not self.sessions[session_id].get("candidate_name"):
            db_s = self._get_db_session(session_id)
            if db_s and db_s.candidate:
                self.sessions[session_id]["candidate_name"] = db_s.candidate.full_name

        return self.sessions[session_id]

    def build_patient_system_prompt(self, content: dict) -> str:
        setting = content.get("setting") or content.get("scenario", {}).get("setting", "Medical Clinic")
        patient = content.get("patient_card", {})
        candidate = content.get("candidate_card", {})
        candidate_role = candidate.get("role", "Nurse")
        patient_role = patient.get("role", "Patient")

        # Patient description
        patient_desc = (
            patient.get("description")
            or content.get("scenario", {}).get("description")
            or "A patient presenting for medical consultation."
        )

        # Patient tasks / concerns
        raw_tasks = patient.get("tasks", [])
        if raw_tasks:
            tasks_text = "\n".join(f"- {t}" for t in raw_tasks)
        else:
            # Fallback for legacy format with concerns and background_information
            fallback_items = []
            for c in patient.get("concerns", []):
                fallback_items.append(f"- Express concern: {c}")
            for b in patient.get("background_information", []):
                fallback_items.append(f"- State symptom: {b}")
            tasks_text = "\n".join(fallback_items) if fallback_items else "- Explain your condition and concerns clearly."

        med_history = "\n".join(f"- {m}" for m in patient.get("medical_history", []))
        history_section = f"\nMEDICAL & FAMILY HISTORY:\n{med_history}\n" if med_history else ""

        return f"""You are role-playing as the patient in a simulated medical consultation.
SETTING: {setting}

PATIENT SITUATION & PROFILE:
{patient_desc}

YOUR TASKS & CONCERNS AS THE PATIENT:
{tasks_text}
{history_section}
RULES FOR YOUR PERFORMANCE:
1. ALWAYS REMAIN IN CHARACTER as the patient. Never speak as an AI, doctor, or nurse.
2. The healthcare professional speaking to you is the {candidate_role}. Address them naturally as '{candidate_role}'.
3. DO NOT DUMP ALL INFORMATION AT ONCE:
   - Only reveal symptoms, background, and history when the {candidate_role.lower()} specifically asks or explores them.
4. CONCISE SPOKEN RESPONSES: Keep your responses to 1-3 conversational spoken sentences (maximum 40 words). This is spoken through voice TTS.
5. EMOTIONAL EXPRESSION: Reflect your assigned situation and personality. If the {candidate_role.lower()} shows warm empathy and explains things clearly, gradually feel reassured. If they use jargon, ask them to explain.
6. ASK YOUR CONCERNS: Naturally express 1 of your tasks or questions when appropriate or when invited to ask questions.
7. NO STAGE DIRECTIONS: Do not include formatting like *sighs* or [nervous tone]. Only output the spoken dialogue.

You must respond in valid JSON with this exact schema:
{{
  "speech": "Your spoken reply to the {candidate_role.lower()}",
  "emotional_state": "anxious" | "reassured" | "relieved" | "confused",
  "concern_raised": "Brief note on concern brought up, or null",
  "is_complete": false
}}
"""

    def build_oet_intro(self) -> str:
        """
        Concise, professional introductory script spoken by the interlocutor before preparation begins.
        Informs the candidate about real test administrative checks without dummy names or locations.
        """
        return (
            "Hello and welcome. This is a practice session for the Occupational English Test speaking sub-test. "
            "Please note that in the real exam, the interlocutor will record an official test announcement, "
            "verify your identification, and conduct a brief warm-up conversation. "
            "For this practice session, we will skip those administrative steps and start directly with your preparation. "
            "You now have three minutes to read your candidate card and prepare for the consultation. "
            "Your preparation time starts now."
        )

    def start_oet_intro(self, session_id: str, question_id: str = None, candidate_name: str = None) -> dict:
        """Initialize the session with the official Interlocutor introduction and preparation setup."""
        lock = self._get_session_lock(session_id)
        with lock:
            session = self.get_or_create_session(session_id, question_id, candidate_name)

            if session.get("state") == RolePlayState.COMPLETED:
                return {
                    "session_id": session_id,
                    "state": RolePlayState.COMPLETED,
                    "is_complete": True,
                    "text": "This consultation has already concluded.",
                    "audio": None,
                    "lipsync": None,
                }

            if session.get("state") == RolePlayState.INTERLOCUTOR_INTRO and session.get("intro_message"):
                return session["intro_message"]

            session["started_at"] = datetime.now(timezone.utc)
            session["state"] = RolePlayState.INTERLOCUTOR_INTRO
            session["phase"] = "interlocutor_intro"
            session["history"] = []

            intro_text = self.build_oet_intro()
            audio_b64, lipsync = synthesize_speech_with_lipsync(intro_text)

            result = {
                "session_id": session_id,
                "phase": "interlocutor_intro",
                "state": RolePlayState.INTERLOCUTOR_INTRO,
                "role": "interlocutor",
                "text": intro_text,
                "intro_text": intro_text,
                "audio": audio_b64,
                "lipsync": lipsync,
                "preparation_time": 180,
                "speaking_time": 300,
                "question": session["question"],
                "is_complete": False,
            }
            session["intro_message"] = result
            return result

    def build_interlocutor_handover(self) -> str:
        """
        Official OET interlocutor script spoken immediately when preparation time completes.
        Hands over the floor to the candidate (Doctor) to start the consultation.
        """
        return (
            "Thank you. The role-play will now last for about five minutes. "
            "Don't worry if I stop you when the time is up. "
            "Can you start the role-play now, please?"
        )

    def start_handover(self, session_id: str, question_id: str = None) -> dict:
        """
        Triggered when preparation time finishes (or candidate clicks 'I'm Ready').
        Interlocutor speaks the official OET instruction asking the doctor to begin the consultation.
        """
        lock = self._get_session_lock(session_id)
        with lock:
            session = self.get_or_create_session(session_id, question_id)

            if session.get("state") == RolePlayState.COMPLETED:
                return {
                    "session_id": session_id,
                    "state": RolePlayState.COMPLETED,
                    "is_complete": True,
                    "text": "This consultation has already concluded.",
                    "audio": None,
                    "lipsync": None,
                }

            session["phase"] = "handover"
            session["state"] = RolePlayState.DOCTOR_TURN
            session["doctor_starts"] = True
            if not session.get("started_at"):
                session["started_at"] = datetime.now(timezone.utc)

            handover_text = self.build_interlocutor_handover()
            audio_b64, lipsync = synthesize_speech_with_lipsync(handover_text)

            result = {
                "session_id": session_id,
                "phase": "handover",
                "state": RolePlayState.DOCTOR_TURN,
                "role": "interlocutor",
                "text": handover_text,
                "audio": audio_b64,
                "lipsync": lipsync,
                "speaking_time": 300,
                "duration": 300,
                "doctor_starts": True,
                "question": session["question"],
                "is_complete": False,
            }
            session["last_handover_message"] = result
            return result

    def build_interlocutor_conclusion(self) -> str:
        """
        Official OET interlocutor script spoken when the 5-minute role-play time ends.
        Signals the official conclusion of the speaking test role-play.
        """
        return "Thank you. That is the end of the role-play."

    def finish_roleplay(self, session_id: str) -> dict:
        """
        Triggered when the 5-minute role-play time stops (or candidate concludes consultation).
        Interlocutor speaks the official concluding script and closes the active consultation phase.
        """
        lock = self._get_session_lock(session_id)
        with lock:
            session = self.get_or_create_session(session_id)

            if session.get("state") == RolePlayState.COMPLETED and session.get("conclusion_message"):
                return session["conclusion_message"]

            session["phase"] = "finished"
            session["state"] = RolePlayState.COMPLETED
            session["completed_at"] = session.get("completed_at") or datetime.now(timezone.utc)

            conclusion_text = self.build_interlocutor_conclusion()
            audio_b64, lipsync = synthesize_speech_with_lipsync(conclusion_text)

            result = {
                "session_id": session_id,
                "phase": "finished",
                "state": RolePlayState.COMPLETED,
                "role": "interlocutor",
                "text": conclusion_text,
                "conclusion_text": conclusion_text,
                "audio": audio_b64,
                "lipsync": lipsync,
                "is_complete": True,
            }
            session["conclusion_message"] = result

            db_session = self._get_db_session(session_id)
            if db_session:
                try:
                    db_session.status = "completed"
                    db_session.completed_at = session["completed_at"]
                    db.session.commit()
                except Exception as e:
                    print(f"Error persisting completion state to DB: {e}")

            return result

    def start_consultation(self, session_id: str, question_id: str = None, candidate_name: str = None) -> dict:
        """Starts the clinical consultation phase where the AI transitions into the Patient persona."""
        lock = self._get_session_lock(session_id)
        with lock:
            session = self.get_or_create_session(session_id, question_id, candidate_name)

            if session.get("state") == RolePlayState.COMPLETED:
                return {
                    "session_id": session_id,
                    "state": RolePlayState.COMPLETED,
                    "is_complete": True,
                    "text": "This consultation has already concluded.",
                    "audio": None,
                    "lipsync": None,
                }

            # If already in active consultation, return cached greeting
            if session.get("state") == RolePlayState.PATIENT_SPEAKING and session.get("last_patient_message"):
                return session["last_patient_message"]

            session["phase"] = "roleplay"
            session["state"] = RolePlayState.PATIENT_SPEAKING
            session["turn_count"] = 1
            if not session.get("started_at"):
                session["started_at"] = datetime.now(timezone.utc)

            candidate_card = session["question"].get("content", {}).get("candidate_card", {})
            patient_card = session["question"].get("content", {}).get("patient_card", {})
            candidate_role = candidate_card.get("role", "Nurse")
            custom_greeting = patient_card.get("initial_greeting")
            initial_emotional_state = patient_card.get("initial_emotional_state", "anxious")

            title = session["question"].get("title", "")
            desc = patient_card.get("description", "")

            if custom_greeting:
                greeting = custom_greeting
            elif "chest" in title.lower() or "chest" in desc.lower():
                greeting = (
                    f"Hello {candidate_role}, thank you for seeing me today. I've been getting this pain in my chest "
                    "over the past few days, and honestly, I'm really anxious and worried about it."
                )
            else:
                greeting = (
                    f"Hello {candidate_role}, thank you for coming to see me today. "
                    "I've been feeling quite worried and really wanted to talk through what is going on."
                )

            audio_b64, lipsync = synthesize_speech_with_lipsync(greeting)

            turn = {
                "role": "patient",
                "text": greeting,
                "emotional_state": initial_emotional_state,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            session["history"].append(turn)

            db_session = self._get_db_session(session_id)
            if db_session:
                try:
                    db_session.status = "in_progress"
                    db_session.stage = 1
                    db_session.transcript = list(session["history"])
                    db_session.started_at = session.get("started_at") or datetime.now(timezone.utc)
                    db.session.commit()
                except Exception as e:
                    print(f"Error persisting initial consultation turn: {e}")

            result = {
                "session_id": session_id,
                "phase": "roleplay",
                "state": RolePlayState.PATIENT_SPEAKING,
                "role": "patient",
                "question": session["question"],
                "text": greeting,
                "patient_text": greeting,
                "audio": audio_b64,
                "lipsync": lipsync,
                "emotional_state": "anxious",
                "turn_count": 1,
                "is_complete": False,
            }
            session["last_patient_message"] = result
            return result

    def start_roleplay(self, session_id: str, question_id: str = None, with_intro: bool = False, candidate_name: str = None) -> dict:
        """
        Initialize the roleplay session.
        If with_intro is True: begins with official Interlocutor intro & preparation setup.
        If with_intro is False: directly initiates clinical patient consultation.
        """
        if with_intro:
            return self.start_oet_intro(session_id, question_id, candidate_name)
        return self.start_consultation(session_id, question_id, candidate_name)

    def transcribe_doctor_audio(self, audio_bytes: bytes, mime_type: str = "audio/webm", session: dict = None) -> str:
        """Transcribe spoken words from doctor audio bytes using Gemini."""
        try:
            response = self.client.models.generate_content(
                model=DEFAULT_MODEL,
                contents=[
                    types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                    "Transcribe the doctor's spoken consultation speech accurately. Return ONLY the transcribed text.",
                ],
            )
            if session:
                self._track_usage(session, response)
            return response.text.strip() if response and response.text else ""
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""

    def process_doctor_speech(
        self,
        session_id: str,
        audio_bytes: bytes = None,
        doctor_text: str = None,
        mime_type: str = "audio/webm",
        on_status=None,
        on_transcript=None,
    ) -> dict:
        """
        Coordinates receiving the Doctor's response, generating the Patient's reaction,
        Kokoro TTS speech synthesis, and turn tracking.
        """
        lock = self._get_session_lock(session_id)
        acquired = lock.acquire(blocking=False)
        if not acquired:
            return {
                "error": "Previous doctor response is still being processed. Please wait.",
                "code": "CONCURRENT_PROCESSING",
                "recoverable": True,
            }

        try:
            session = self.get_or_create_session(session_id)

            if session.get("state") == RolePlayState.COMPLETED:
                return {
                    "error": "Consultation has already concluded.",
                    "code": "CONSULTATION_COMPLETED",
                    "recoverable": False,
                }

            session["is_processing"] = True
            session["state"] = RolePlayState.PROCESSING_SPEECH

            # 1. Transcribe or extract doctor speech
            effective_text = ""
            if audio_bytes:
                if on_status:
                    on_status("transcribing_audio", "Transcribing doctor's voice...")
                effective_text = self.transcribe_doctor_audio(audio_bytes, mime_type, session=session)
                if not effective_text:
                    effective_text = "(Doctor spoke unclearly)"
                if on_transcript:
                    on_transcript(effective_text)
            elif doctor_text is not None and str(doctor_text).strip():
                effective_text = str(doctor_text).strip()
            else:
                session["is_processing"] = False
                session["state"] = RolePlayState.DOCTOR_LISTENING
                return {
                    "error": "Missing doctor speech or text.",
                    "code": "MISSING_INPUT",
                    "recoverable": True,
                }

            if not session.get("started_at"):
                session["started_at"] = datetime.now(timezone.utc)

            # 2. Record doctor turn
            doctor_turn = {
                "role": "doctor",
                "text": effective_text,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            session["history"].append(doctor_turn)
            session["turn_count"] += 1

            if on_status:
                on_status("generating_response", "Patient is listening and formulating response...")

            # 3. Formulate Patient Reply with Gemini
            system_prompt = self.build_patient_system_prompt(session["question"].get("content", {}))

            conversation_log = "\n".join(
                f"{t['role'].upper()}: {t['text']}" for t in session["history"]
            )

            prompt = f"""CONSULTATION HISTORY:
{conversation_log}

The Doctor just said to you: "{effective_text}"

TASK:
Respond as the patient according to your profile, personality, and rules.
Remember: 1-3 short spoken sentences. Answer what was asked; express emotional reaction naturally.
"""

            patient_speech = ""
            emotional_state = "anxious"

            for model_name in [DEFAULT_MODEL, "gemini-3.5-flash", "gemini-3.5-flash-lite"]:
                try:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            response_mime_type="application/json",
                            temperature=0.7,
                        ),
                    )
                    data = json.loads(response.text.strip())
                    patient_speech = data.get("speech", "").strip()
                    emotional_state = data.get("emotional_state", "anxious")
                    self._track_usage(session, response)
                    if patient_speech:
                        break
                except Exception as e:
                    print(f"Patient generation error with {model_name}: {e}")
                    continue

            if not patient_speech:
                patient_speech = (
                    "I understand, Doctor. It's just very concerning for me. "
                    "Do you think I need to have my heart tested right away?"
                )

            # 4. Synthesize Patient speech with Kokoro TTS
            if on_status:
                on_status("synthesizing_speech", "Synthesizing patient voice...")

            audio_b64, lipsync = synthesize_speech_with_lipsync(patient_speech)

            patient_turn = {
                "role": "patient",
                "text": patient_speech,
                "emotional_state": emotional_state,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            session["history"].append(patient_turn)

            # 5. Persist to DB if applicable
            db_session = self._get_db_session(session_id)
            if db_session:
                try:
                    db_session.stage = session["turn_count"]
                    db_session.transcript = list(session["history"])
                    db.session.commit()
                except Exception as e:
                    print(f"Error updating DB session: {e}")

            session["state"] = RolePlayState.PATIENT_SPEAKING
            session["is_processing"] = False

            result = {
                "session_id": session_id,
                "state": RolePlayState.PATIENT_SPEAKING,
                "role": "patient",
                "turn_count": session["turn_count"],
                "doctor_text": effective_text,
                "text": patient_speech,
                "audio": audio_b64,
                "lipsync": lipsync,
                "emotional_state": emotional_state,
                "is_complete": False,
            }
            session["last_patient_message"] = result
            return result

        except Exception as e:
            print(f"Error in process_doctor_speech for {session_id}: {e}")
            session = self.sessions.get(session_id)
            if session:
                session["is_processing"] = False
                session["state"] = RolePlayState.DOCTOR_LISTENING
            return {
                "error": "Failed to process doctor speech.",
                "code": "PROCESSING_ERROR",
                "recoverable": True,
            }
        finally:
            lock.release()

    def evaluate_roleplay(self, session_id: str) -> dict:
        """
        Generates an OET / Clinical Consultation Scorecard evaluating the Candidate's
        communication, empathy, structure, and clinical investigation explanation
        strictly against official OET Speaking standards and candidate card tasks.
        """
        lock = self._get_session_lock(session_id)
        with lock:
            session = self.get_or_create_session(session_id)
            if session.get("evaluation_result"):
                return session["evaluation_result"]

            content = session["question"].get("content", {})
            candidate_card = content.get("candidate_card", {})
            candidate_role = candidate_card.get("role", "Nurse")
            raw_tasks = candidate_card.get("tasks") or candidate_card.get("instructions", [])
            instructions = "\n".join(f"- {i}" for i in raw_tasks)
            setting = content.get("setting") or content.get("scenario", {}).get("setting", "Medical Clinic")
            cand_desc = candidate_card.get("description") or content.get("scenario", {}).get("description", "")

            # 1. Compute consultation engagement metrics
            candidate_turns = [
                t for t in session.get("history", [])
                if t.get("role", "").lower() in ("doctor", "nurse", "candidate")
            ]
            candidate_turn_count = len(candidate_turns)
            candidate_word_count = sum(len(t.get("text", "").split()) for t in candidate_turns)

            if not session.get("completed_at"):
                session["completed_at"] = datetime.now(timezone.utc)

            started_at = session.get("started_at")
            completed_at = session["completed_at"]

            if started_at:
                actual_duration = max(0, int((completed_at - started_at).total_seconds()))
                # If duration was extremely short (< 5 seconds) but candidate had turns (e.g. fast replay/unit test),
                # estimate realistic speaking duration based on candidate turns (~25s per turn).
                duration_seconds = max(actual_duration, candidate_turn_count * 25) if candidate_turn_count > 0 else actual_duration
            else:
                duration_seconds = candidate_turn_count * 25

            mins = duration_seconds // 60
            secs = duration_seconds % 60
            duration_formatted = f"{mins}m {secs:02d}s"

            # 2. Early gate for abandoned or zero-participation consultations
            if candidate_turn_count == 0 or (candidate_turn_count == 1 and candidate_word_count < 10 and duration_seconds < 40):
                scorecard = {
                    "overall_score": 1.0,
                    "oet_grade": "E",
                    "information_gathering_score": 1,
                    "empathy_and_reassurance_score": 1,
                    "explanation_clarity_score": 1,
                    "checking_understanding_score": 1,
                    "clinical_tasks_achieved": [],
                    "clinical_tasks_missed": list(raw_tasks),
                    "strengths": ["Attended the role-play session."],
                    "areas_for_improvement": [
                        "Candidate did not speak or actively engage in the consultation.",
                        "In OET Speaking, you must sustain a 5-minute interaction with the patient.",
                        "Actively introduce yourself and systematically explore the patient's concerns.",
                    ],
                    "summary": (
                        f"The consultation was discontinued prematurely after {duration_formatted} "
                        f"with {candidate_turn_count} candidate response(s) ({candidate_word_count} words). "
                        "In the OET speaking sub-test, candidates are expected to sustain a 5-minute clinical consultation. "
                        "None of the required clinical tasks could be assessed."
                    ),
                    "duration_seconds": duration_seconds,
                    "candidate_turn_count": candidate_turn_count,
                    "candidate_word_count": candidate_word_count,
                }
            else:
                # 3. Format full transcript with explicit speaker labels matching candidate role
                formatted_transcript = []
                for t in session.get("history", []):
                    role_raw = t.get("role", "").lower()
                    if role_raw in ("doctor", "nurse", "candidate"):
                        display_role = candidate_role.upper()
                    else:
                        display_role = "PATIENT"
                    formatted_transcript.append(f"{display_role}: {t.get('text', '')}")
                conversation_log = "\n".join(formatted_transcript)

                is_premature = duration_seconds < 180 or candidate_turn_count < 5

                prompt = f"""You are a senior clinical educator and official OET (Occupational English Test) medical communication examiner.
Evaluate the candidate's clinical consultation performance as the {candidate_role} speaking to a patient.

SETTING: {setting}
CLINICAL SCENARIO:
{session['question'].get('title')}
{cand_desc}

CANDIDATE'S CLINICAL OBJECTIVES:
{instructions}

CONSULTATION TIME & ENGAGEMENT METRICS:
- Target Speaking Duration: 300 seconds (5 minutes)
- Actual Elapsed Duration: {duration_seconds} seconds ({duration_formatted})
- Candidate Turns Taken: {candidate_turn_count}
- Total Candidate Words Spoken: {candidate_word_count}
- Consultation Pacing: {"PREMATURELY TERMINATED (Under 3 minutes or fewer than 5 turns)" if is_premature else "SUSTAINED CONSULTATION"}

FULL CONSULTATION TRANSCRIPT:
{conversation_log}

TASK & OET EVALUATION CRITERIA:
Evaluate the candidate strictly according to official OET clinical communication criteria:
1. Relationship Building (establishing rapport, listening, demonstrating empathy and respect)
2. Understanding & Incorporating Patient Perspective (exploring patient concerns and anxiety)
3. Providing Structure (purposeful sequencing, signposting, organizing consultation flow)
4. Information Gathering (open to closed questions, clarifying symptoms, active listening)
5. Information Giving (clear explanations, avoiding jargon, checking understanding)

CRITICAL OET GRADING RULES:
1. DURATION & COMPLETENESS PENALTY:
   - In official OET, candidate speaking time is 5 minutes (300 seconds).
   - If the consultation lasted under 3 minutes (< 180 seconds) or candidate took fewer than 6 speaking turns or spoke fewer than 100 words:
     * The candidate MUST NOT be awarded Grade A (9.0-10) or Grade B (7.0-8.9).
     * The MAXIMUM allowable grade is Grade D (3.0 - 4.9), or Grade E (1.0 - 2.9) if very brief (< 1.5 minutes or < 3 turns).
     * The summary must explicitly state that the consultation was cut short before clinical tasks could be established.
2. RIGOROUS CLINICAL OBJECTIVES CHECK:
   - Check every single item in the CANDIDATE'S CLINICAL OBJECTIVES list against the transcript.
   - ONLY list an item under "clinical_tasks_achieved" if there is explicit, direct evidence in the transcript that the candidate addressed it.
   - Every single objective that was not attempted or not completed MUST be placed in "clinical_tasks_missed".
   - If the consultation was stopped early, all uncompleted objectives on the card MUST be in "clinical_tasks_missed".
3. NO HALLUCINATION OF COMPETENCE:
   - Do NOT invent or assume empathy, explanation, or questions that the candidate did not actually speak.
   - Score strictly on candidate's demonstrated speech.
4. SCORING SCALE:
   - Grade A (9.0 - 10.0): Exceptional. Achieved all tasks, sustained 4.5 - 5 minutes, excellent clinical communication.
   - Grade B (7.0 - 8.9): Pass Standard. Achieved almost all tasks, sustained ~4 - 5 minutes, effective clinical communication.
   - Grade C+ (6.0 - 6.9): Fair. 1-2 missed tasks, sustained ~3.5 - 4 minutes.
   - Grade C (5.0 - 5.9): Marginally adequate. Multiple tasks missed, or ended around 2.5 - 3 minutes.
   - Grade D (3.0 - 4.9): Weak / Insufficient. Ended early (< 3 minutes or < 6 turns), most tasks missed.
   - Grade E (1.0 - 2.9): Very poor / Abandoned. Ended very early (< 1.5 minutes or < 3 turns), almost all tasks missed.

Respond with valid JSON matching this schema:
{{
  "overall_score": <number between 1.0 and 10.0>,
  "oet_grade": "<'A' | 'B' | 'C+' | 'C' | 'D' | 'E'>",
  "information_gathering_score": <integer from 1 to 10>,
  "empathy_and_reassurance_score": <integer from 1 to 10>,
  "explanation_clarity_score": <integer from 1 to 10>,
  "checking_understanding_score": <integer from 1 to 10>,
  "clinical_tasks_achieved": ["<task explicitly achieved in transcript>"],
  "clinical_tasks_missed": ["<task not achieved>"],
  "strengths": ["<genuine strength observed in candidate speech>"],
  "areas_for_improvement": ["<specific actionable clinical communication feedback>"],
  "summary": "<critical 3-4 sentence evaluation referencing duration, tasks achieved/missed, and OET communication standards>"
}}
"""

                scorecard = None
                for model_name in [DEFAULT_MODEL, "gemini-3.5-flash", "gemini-3.5-flash-lite"]:
                    try:
                        response = self.client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                temperature=0.3,
                            ),
                        )
                        scorecard = json.loads(response.text.strip())
                        self._track_usage(session, response)
                        if scorecard:
                            break
                    except Exception as e:
                        print(f"Scorecard generation error with {model_name}: {e}")
                        continue

                # Realistic fallback based on actual engagement if LLM generation fails
                if not scorecard:
                    if candidate_turn_count < 3 or duration_seconds < 90 or candidate_word_count < 50:
                        fallback_grade = "E"
                        fallback_score = 2.0
                        fallback_subscore = 2
                        achieved = []
                        missed = list(raw_tasks)
                        summary = (
                            f"The consultation concluded prematurely after {duration_formatted} "
                            f"with only {candidate_turn_count} candidate turn(s). Insufficient evidence to demonstrate "
                            "clinical communication competence according to OET standards."
                        )
                    elif candidate_turn_count < 6 or duration_seconds < 180:
                        fallback_grade = "D"
                        fallback_score = 4.0
                        fallback_subscore = 4
                        achieved = [raw_tasks[0]] if raw_tasks else ["Initial introduction"]
                        missed = raw_tasks[1:] if len(raw_tasks) > 1 else []
                        summary = (
                            f"The consultation lasted {duration_formatted} ({candidate_turn_count} turns), which is shorter "
                            "than the required 5 minutes. Several clinical tasks could not be completed."
                        )
                    else:
                        fallback_grade = "C+"
                        fallback_score = 6.5
                        fallback_subscore = 6
                        half = max(1, len(raw_tasks) // 2)
                        achieved = raw_tasks[:half]
                        missed = raw_tasks[half:]
                        summary = (
                            f"Consultation completed ({duration_formatted}, {candidate_turn_count} turns). "
                            "Detailed automated evaluation temporarily unavailable; estimated score based on conversation length."
                        )

                    scorecard = {
                        "overall_score": fallback_score,
                        "oet_grade": fallback_grade,
                        "information_gathering_score": fallback_subscore,
                        "empathy_and_reassurance_score": fallback_subscore,
                        "explanation_clarity_score": fallback_subscore,
                        "checking_understanding_score": fallback_subscore,
                        "clinical_tasks_achieved": achieved,
                        "clinical_tasks_missed": missed,
                        "strengths": ["Completed speaking turns during consultation."] if candidate_turn_count > 0 else ["Attended session."],
                        "areas_for_improvement": [
                            "Maintain consultation for the full 5-minute speaking time.",
                            "Address all clinical tasks on the candidate card systematically.",
                        ],
                        "summary": summary,
                    }

                scorecard["duration_seconds"] = duration_seconds
                scorecard["candidate_turn_count"] = candidate_turn_count
                scorecard["candidate_word_count"] = candidate_word_count

            session["scorecard"] = scorecard
            session["state"] = RolePlayState.COMPLETED
            session["completed_at"] = completed_at

            self._log_session_cost(session)

            farewell = (
                f"Thank you {candidate_role}. That concludes our consultation. I appreciate your advice and care."
                if candidate_turn_count >= 2
                else f"Thank you {candidate_role}. That concludes our session."
            )
            audio_b64, lipsync = synthesize_speech_with_lipsync(farewell)

            # Persist completion to DB
            db_session = self._get_db_session(session_id)
            if db_session:
                try:
                    db_session.status = "completed"
                    db_session.completed_at = session["completed_at"]
                    db_session.scorecard = scorecard
                    db.session.commit()
                except Exception as e:
                    print(f"Error persisting roleplay scorecard: {e}")

            # Log full session token usage and estimated cost to the server console
            self._log_session_cost(session)

            result = {
                "session_id": session_id,
                "state": RolePlayState.COMPLETED,
                "is_complete": True,
                "text": farewell,
                "audio": audio_b64,
                "lipsync": lipsync,
                "scorecard": scorecard,
                "transcript": session["history"],
            }
            session["evaluation_result"] = result
            return result


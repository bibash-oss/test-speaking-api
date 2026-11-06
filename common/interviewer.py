import os
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
from google import genai
from google.genai import types
from common.tts import synthesize_speech_with_lipsync

load_dotenv()

DEFAULT_MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """You are a professional, warm, and attentive job interviewer.
Your goal is to conduct a natural, engaging, structured interview with the candidate.

RULES:
1. Ask ONLY ONE question at a time.
2. Keep questions concise and conversational (1-3 sentences maximum).
3. Briefly acknowledge or react naturally to what the candidate just said before asking the next question.
4. Do not repeat questions or overwhelm the candidate.
5. Calibrate the question difficulty strictly according to the target seniority level.
6. Reference the candidate's actual background or resume projects when relevant.
7. Interview structure typically covers:
   - Warm welcome & introduction
   - Technical / project deep-dive (based on resume & job requirements)
   - Problem solving / challenge faced
   - Behavioral or situational scenario
   - Wrap-up & closing
8. When the interview is complete (usually after 4-5 questions), thank the candidate warmly and conclude.

You must respond in valid JSON matching this schema:
{
  "acknowledgement": "Brief natural reaction to the candidate's last answer (optional, empty if starting)",
  "question": "The question to ask the candidate, or closing farewell if ending",
  "is_complete": false
}
"""

LEVEL_GUIDELINES = {
    "intern": "Focus on fundamentals, curiosity, academic/hobby projects, and eagerness to learn. Keep tone warm and encouraging.",
    "junior": "Focus on practical coding concepts, standard frameworks/tools, debugging basics, and team collaboration.",
    "mid-level": "Focus on independent feature delivery, trade-offs, testing, component design, and debugging production issues.",
    "senior": "Focus on system design at scale, distributed architecture, mentoring, resilience, and high-impact trade-offs.",
    "lead": "Focus on engineering vision, high-stakes system decisions, cross-functional leadership, and technical strategy.",
}

DEFAULT_TOTAL_STAGES = int(os.getenv("TOTAL_INTERVIEW_STAGES", "5"))


class InterviewState:
    READY = "ready"
    INTERVIEWER_SPEAKING = "interviewer_speaking"
    CANDIDATE_LISTENING = "candidate_listening"
    PROCESSING_ANSWER = "processing_answer"
    COMPLETED = "completed"
    ERROR = "error"


class InterviewManager:
    def __init__(self, api_key: str = None):
        import threading
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        # In-memory fallback for ad-hoc / test sessions: session_id -> dict
        self.sessions = {}
        self._session_locks = {}
        self._meta_lock = threading.Lock()

    def parse_resume(self, file_bytes: bytes, filename: str = "") -> str:
        """Extract and structure resume text using pypdf and Gemini AI."""
        extracted_text = ""
        is_pdf = filename.lower().endswith(".pdf") or file_bytes.startswith(b"%PDF")

        # 1. Try fast local PDF text extraction via pypdf
        if is_pdf:
            try:
                import io
                from pypdf import PdfReader
                reader = PdfReader(io.BytesIO(file_bytes))
                pages_text = []
                for page in reader.pages:
                    txt = page.extract_text()
                    if txt:
                        pages_text.append(txt)
                if pages_text:
                    extracted_text = "\n".join(pages_text).strip()
            except Exception as e:
                print(f"pypdf extraction notice: {e}")

        # 2. Plain text or UTF-8 fallback if not PDF
        if not extracted_text and not is_pdf:
            try:
                extracted_text = file_bytes.decode("utf-8", errors="ignore").strip()
            except Exception:
                pass

        # 3. Use Gemini to structure and summarize for the interviewer
        try:
            prompt = (
                "You are an expert technical interviewer assistant. Analyze this candidate's resume/CV "
                "and extract a structured profile for the interviewer.\n\n"
                "Format as follows:\n"
                "• Summary: (2-3 sentences of overall background & seniority)\n"
                "• Core Technical Skills: (Languages, frameworks, databases, tools)\n"
                "• Key Experience & Projects: (Key roles, achievements, architecture highlights)\n"
                "• Education & Certifications: (Degree, certifications if any)\n\n"
                "Keep it clean, concise, and professional without markdown tables."
            )

            if extracted_text:
                # Text extracted from PDF or text file
                response = self.client.models.generate_content(
                    model=DEFAULT_MODEL,
                    contents=[prompt, f"CANDIDATE RESUME CONTENT:\n{extracted_text[:12000]}"],
                )
            elif is_pdf:
                # Scanned or image-based PDF: Send raw PDF bytes directly to Gemini multimodal OCR
                response = self.client.models.generate_content(
                    model=DEFAULT_MODEL,
                    contents=[
                        types.Part.from_bytes(data=file_bytes, mime_type="application/pdf"),
                        prompt,
                    ],
                )
            else:
                return extracted_text

            if response and response.text:
                return response.text.strip()
            return extracted_text
        except Exception as e:
            print(f"Gemini resume parsing error: {e}")
            return extracted_text

    def parse_resume_pdf(self, pdf_bytes: bytes) -> str:
        """Backwards-compatible alias for parse_resume."""
        return self.parse_resume(pdf_bytes, "resume.pdf")

    def evaluate_interview(
        self,
        candidate_name: str,
        role: str,
        level: str,
        job_description: str,
        resume_summary: str,
        history: list,
    ) -> dict:
        """Generate a structured evaluation scorecard at the end of the interview."""
        conversation_log = "\n".join(
            f"{turn.get('role', 'Speaker').capitalize()}: {turn.get('text', '')}"
            for turn in history
        )

        prompt = f"""You are an expert hiring committee lead evaluating an interview.

CANDIDATE: {candidate_name}
TARGET ROLE: {level} {role}

JOB DESCRIPTION REQUIREMENTS:
{job_description or "Standard software engineering requirements"}

CANDIDATE RESUME HIGHLIGHTS:
{resume_summary or "No resume provided"}

INTERVIEW TRANSCRIPT:
{conversation_log}

TASK:
Provide a rigorous, constructive assessment of the candidate's interview performance.
Respond with valid JSON matching this schema:
{{
  "overall_score": 8.0,
  "recommendation": "Strong Hire" | "Hire" | "Borderline" | "Do Not Hire",
  "technical_depth_score": 8,
  "communication_score": 8,
  "problem_solving_score": 8,
  "strengths": ["Clear explanation of concurrency", "Good communication"],
  "concerns": ["Lacked depth on database indexing"],
  "summary": "3-4 sentence comprehensive hiring summary"
}}
"""
        for m in [DEFAULT_MODEL, "gemini-3.5-flash", "gemini-3.5-flash-lite"]:
            try:
                response = self.client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.3,
                    ),
                )
                return json.loads(response.text.strip())
            except Exception as e:
                print(f"Evaluation generation error with {m}: {e}")
                continue

        return {
                "overall_score": 7.0,
                "recommendation": "Review Needed",
                "technical_depth_score": 7,
                "communication_score": 7,
                "problem_solving_score": 7,
                "strengths": ["Completed interview turns"],
                "concerns": ["Automated evaluation encountered an error"],
                "summary": "Candidate completed the interview; manual review recommended.",
            }

    def _get_db_session(self, session_id: str):
        """Helper to find an InterviewSession model if exists."""
        try:
            from models.interview_sessions import InterviewSession
            return InterviewSession.query.filter_by(session_token=session_id).first()
        except Exception:
            return None

    def _get_session_lock(self, session_id: str):
        """Get or create a threading lock for a session."""
        with self._meta_lock:
            if session_id not in self._session_locks:
                import threading
                self._session_locks[session_id] = threading.Lock()
            return self._session_locks[session_id]

    def get_or_create_session(
        self,
        session_id: str,
        role: str = "Software Engineer",
        level: str = "Junior",
        total_stages: int = None,
    ):
        if session_id not in self.sessions:
            # Check if this is a registered database interview session
            db_session = self._get_db_session(session_id)
            if db_session:
                cand = db_session.candidate
                job = cand.job if cand else None
                s_role = job.title if job else role or "Software Engineer"
                s_level = job.level if job else level or "Junior"
                s_name = cand.full_name if cand else "Candidate"
                s_jd = job.description if job else ""
                s_resume = cand.resume_text if cand else ""
                company = job.company_name if job else "our company"
                history = list(db_session.transcript or [])
                answered = sum(1 for turn in history if turn.get("role") == "candidate")
                status = db_session.status or "pending"

                if status == "completed":
                    state = InterviewState.COMPLETED
                elif status == "in_progress":
                    last_turn = history[-1] if history else None
                    if last_turn and last_turn.get("role") == "interviewer":
                        state = InterviewState.CANDIDATE_LISTENING
                    else:
                        state = InterviewState.READY
                else:
                    state = InterviewState.READY

                last_msg = None
                if history:
                    for turn in reversed(history):
                        if turn.get("role") == "interviewer":
                            last_msg = {
                                "session_id": session_id,
                                "stage": db_session.stage or 1,
                                "role": s_role,
                                "level": s_level,
                                "text": turn.get("text", ""),
                                "audio": None,
                                "lipsync": None,
                                "is_complete": (state == InterviewState.COMPLETED),
                            }
                            break

                self.sessions[session_id] = {
                    "role": s_role,
                    "level": s_level,
                    "job_description": s_jd,
                    "resume_summary": s_resume,
                    "company": company,
                    "candidate_name": s_name,
                    "history": history,
                    "stage": db_session.stage or 0,
                    "total_stages": total_stages or DEFAULT_TOTAL_STAGES,
                    "answered_stages": answered,
                    "state": state,
                    "last_interviewer_message": last_msg,
                    "is_processing": False,
                }
            else:
                self.sessions[session_id] = {
                    "role": role or "Software Engineer",
                    "level": level or "Junior",
                    "job_description": "",
                    "resume_summary": "",
                    "company": "our company",
                    "candidate_name": "Candidate",
                    "history": [],
                    "stage": 0,
                    "total_stages": total_stages or DEFAULT_TOTAL_STAGES,
                    "answered_stages": 0,
                    "state": InterviewState.READY,
                    "last_interviewer_message": None,
                    "is_processing": False,
                }
        return self.sessions[session_id]

    def get_session_state(self, session_id: str) -> dict:
        session = self.get_or_create_session(session_id)
        return {
            "session_id": session_id,
            "state": session.get("state", InterviewState.READY),
            "stage": session.get("stage", 0),
            "total_stages": session.get("total_stages", DEFAULT_TOTAL_STAGES),
            "answered_stages": session.get("answered_stages", 0),
            "is_complete": session.get("state") == InterviewState.COMPLETED,
            "last_message": session.get("last_interviewer_message"),
            "role": session.get("role"),
            "level": session.get("level"),
            "company": session.get("company"),
            "candidate_name": session.get("candidate_name"),
            "job_description": session.get("job_description"),
        }

    def is_processing(self, session_id: str) -> bool:
        session = self.sessions.get(session_id)
        if not session:
            return False
        return session.get("is_processing", False)

    def is_completed(self, session_id: str) -> bool:
        state_info = self.get_session_state(session_id)
        return state_info.get("state") == InterviewState.COMPLETED

    def set_candidate_turn(self, session_id: str) -> dict:
        lock = self._get_session_lock(session_id)
        with lock:
            session = self.get_or_create_session(session_id)
            if session.get("state") == InterviewState.INTERVIEWER_SPEAKING:
                session["state"] = InterviewState.CANDIDATE_LISTENING
            return {
                "session_id": session_id,
                "state": session.get("state"),
                "stage": session.get("stage", 0),
                "total_stages": session.get("total_stages", DEFAULT_TOTAL_STAGES),
                "answered_stages": session.get("answered_stages", 0),
            }

    def start_interview(
        self,
        session_id: str,
        role: str = None,
        level: str = None,
        total_stages: int = None,
        candidate_name: str = None,
    ):
        lock = self._get_session_lock(session_id)
        with lock:
            session = self.get_or_create_session(session_id, role, level, total_stages)

            # 1. Reject if already completed
            if session.get("state") == InterviewState.COMPLETED:
                return {
                    "session_id": session_id,
                    "state": InterviewState.COMPLETED,
                    "stage": session.get("stage", 0),
                    "total_stages": session.get("total_stages", DEFAULT_TOTAL_STAGES),
                    "answered_stages": session.get("answered_stages", 0),
                    "is_complete": True,
                    "message": "Interview has already been completed.",
                    "text": "This interview has concluded. Thank you!",
                    "audio": None,
                    "lipsync": None,
                }

            # 2. Reconnection / idempotent start: if already in progress with a message, restore it
            if (
                session.get("state") in (InterviewState.INTERVIEWER_SPEAKING, InterviewState.CANDIDATE_LISTENING)
                and session.get("last_interviewer_message")
                and session.get("stage", 0) >= 1
            ):
                last_msg = dict(session["last_interviewer_message"])
                last_msg["state"] = session["state"]
                last_msg["total_stages"] = session.get("total_stages", DEFAULT_TOTAL_STAGES)
                last_msg["answered_stages"] = session.get("answered_stages", 0)
                return last_msg

            # 3. New interview startup
            db_session = self._get_db_session(session_id)
            if db_session and db_session.candidate and db_session.candidate.job:
                cand = db_session.candidate
                job = cand.job
                role = role or job.title
                level = level or job.level
                candidate_name = candidate_name or cand.full_name
                jd = job.description
                resume_summary = cand.resume_text or ""
                company = job.company_name or "our company"

                db_session.status = "in_progress"
                db_session.stage = 1
                db_session.started_at = datetime.now(timezone.utc)
                cand.status = "in_progress"
            else:
                role = role or "Software Engineer"
                level = level or "Junior"
                candidate_name = candidate_name or "Candidate"
                jd = ""
                resume_summary = ""
                company = "our company"

            session["role"] = role
            session["level"] = level
            session["candidate_name"] = candidate_name
            session["job_description"] = jd
            session["resume_summary"] = resume_summary
            session["company"] = company
            session["history"] = []
            session["stage"] = 1
            session["total_stages"] = total_stages or session.get("total_stages") or DEFAULT_TOTAL_STAGES
            session["answered_stages"] = 0
            session["state"] = InterviewState.INTERVIEWER_SPEAKING

            greeting_name = f", {candidate_name.split()[0]}" if candidate_name and candidate_name != "Candidate" else ""

            r_str = (role or "").strip()
            l_str = (level or "").strip()
            r_lower = r_str.lower()
            l_lower = l_str.lower()

            level_keywords = ["intern", "junior", "mid-level", "mid level", "senior", "lead", "principal", "director"]
            role_already_has_level = any(k in r_lower for k in level_keywords)

            if not l_str or l_lower in r_lower or role_already_has_level:
                position_title = r_str
            else:
                position_title = f"{l_str} {r_str}".strip()

            at_company = ""
            if company and company.strip().lower() not in ("ktmbees", "ktmbees practice", "company", "our company", ""):
                at_company = f" at {company.strip()}"

            greeting = (
                f"Hello{greeting_name}! Welcome to your interview today for the {position_title} position{at_company}. "
                "To kick things off, could you please introduce yourself "
                "and share a little about your background?"
            )

            turn = {"role": "interviewer", "text": greeting}
            session["history"].append(turn)

            # Save to DB if persistent session
            if db_session:
                try:
                    from models import db
                    db_session.transcript = [turn]
                    db.session.commit()
                except Exception as e:
                    print(f"Error saving initial turn to DB: {e}")

            # Synthesize greeting speech
            audio_b64, lipsync = synthesize_speech_with_lipsync(greeting)

            result = {
                "session_id": session_id,
                "state": InterviewState.INTERVIEWER_SPEAKING,
                "stage": 1,
                "total_stages": session["total_stages"],
                "answered_stages": 0,
                "role": role,
                "level": level,
                "text": greeting,
                "audio": audio_b64,
                "lipsync": lipsync,
                "is_complete": False,
            }
            session["last_interviewer_message"] = result
            return result

    def transcribe_audio(self, audio_bytes: bytes, mime_type: str = "audio/webm") -> str:
        """Use Gemini to transcribe audio bytes into text."""
        try:
            response = self.client.models.generate_content(
                model=DEFAULT_MODEL,
                contents=[
                    types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                    "Transcribe the spoken words in this audio recording accurately. Return ONLY the transcribed text, without commentary.",
                ],
            )
            return response.text.strip() if response and response.text else ""
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""

    def process_candidate_speech(
        self,
        session_id: str,
        audio_bytes: bytes = None,
        candidate_text: str = None,
        mime_type: str = "audio/webm",
        on_status=None,
        on_transcript=None,
    ) -> dict:
        """
        Unified handler for candidate audio or text submission.
        Coordinates transcription, question generation, Kokoro TTS, and completion lifecycle.
        """
        lock = self._get_session_lock(session_id)
        acquired = lock.acquire(blocking=False)
        if not acquired:
            return {
                "error": "An answer is currently being processed for this session. Please wait.",
                "code": "CONCURRENT_PROCESSING",
                "recoverable": True,
            }

        try:
            session = self.get_or_create_session(session_id)

            # 1. Validate session state
            if session.get("state") == InterviewState.COMPLETED:
                return {
                    "error": "Interview has already been completed.",
                    "code": "SESSION_COMPLETED",
                    "recoverable": False,
                }

            session["is_processing"] = True
            session["state"] = InterviewState.PROCESSING_ANSWER

            # 2. Extract or transcribe candidate answer
            effective_text = ""
            if audio_bytes:
                if on_status:
                    on_status("transcribing_audio", "Transcribing candidate audio...")
                effective_text = self.transcribe_audio(audio_bytes, mime_type=mime_type)
                if not effective_text:
                    effective_text = "(Unclear audio response)"
                if on_transcript:
                    on_transcript(effective_text)
            elif candidate_text is not None and str(candidate_text).strip():
                effective_text = str(candidate_text).strip()
            else:
                session["is_processing"] = False
                session["state"] = InterviewState.CANDIDATE_LISTENING
                return {
                    "error": "Missing candidate audio or text",
                    "code": "MISSING_INPUT",
                    "recoverable": True,
                }

            # 3. Record candidate turn
            candidate_turn = {"role": "candidate", "text": effective_text}
            session["history"].append(candidate_turn)
            session["answered_stages"] = session.get("answered_stages", 0) + 1
            total_stages = session.get("total_stages") or DEFAULT_TOTAL_STAGES

            # 4. Check if interview turn sequence has reached completion
            is_complete = session["answered_stages"] >= total_stages

            db_session = self._get_db_session(session_id)

            if is_complete:
                # ── FINAL COMPLETION FLOW ──
                if on_status:
                    on_status("evaluating_interview", "Generating post-interview evaluation...")

                scorecard = self.evaluate_interview(
                    candidate_name=session.get("candidate_name", "Candidate"),
                    role=session["role"],
                    level=session["level"],
                    job_description=session.get("job_description", ""),
                    resume_summary=session.get("resume_summary", ""),
                    history=session["history"],
                )

                cand_first = session.get("candidate_name", "").split()[0] if session.get("candidate_name") and session.get("candidate_name") != "Candidate" else ""
                greeting_name = f", {cand_first}" if cand_first else ""
                farewell = (
                    f"Thank you so much{greeting_name}! That concludes all the questions for your interview today. "
                    "We really appreciate your time and thoughtful responses. Our hiring team will review your "
                    "performance evaluation and get in touch soon. Have a wonderful day!"
                )

                if on_status:
                    on_status("synthesizing_speech", "Synthesizing closing message...")

                audio_b64, lipsync = synthesize_speech_with_lipsync(farewell)

                interviewer_turn = {"role": "interviewer", "text": farewell}
                session["history"].append(interviewer_turn)

                if db_session:
                    try:
                        from models import db
                        db_session.stage = session["stage"]
                        db_session.transcript = list(session["history"])
                        db_session.scorecard = scorecard
                        db_session.status = "completed"
                        db_session.completed_at = datetime.now(timezone.utc)
                        if db_session.candidate:
                            db_session.candidate.status = "completed"
                        db.session.commit()
                    except Exception as e:
                        print(f"Error updating DB session on complete: {e}")

                session["state"] = InterviewState.COMPLETED
                session["is_processing"] = False

                result = {
                    "session_id": session_id,
                    "state": InterviewState.COMPLETED,
                    "stage": session["stage"],
                    "total_stages": total_stages,
                    "answered_stages": session["answered_stages"],
                    "candidate_text": effective_text,
                    "text": farewell,
                    "audio": audio_b64,
                    "lipsync": lipsync,
                    "is_complete": True,
                    "scorecard": scorecard,
                    "message": "Your interview has been completed.",
                }
                session["last_interviewer_message"] = result
                return result

            else:
                # ── NEXT QUESTION GENERATION FLOW ──
                session["stage"] += 1

                if on_status:
                    on_status("generating_question", "Analyzing response and formulating next question...")

                level_key = session.get("level", "junior").lower()
                level_guidance = LEVEL_GUIDELINES.get(level_key, LEVEL_GUIDELINES["junior"])

                conversation_log = "\n".join(
                    f"{turn['role'].capitalize()}: {turn['text']}" for turn in session["history"]
                )

                prompt = f"""TARGET ROLE: {session['role']}
SENIORITY LEVEL: {session['level']}
LEVEL GUIDANCE: {level_guidance}
CANDIDATE NAME: {session.get('candidate_name', 'Candidate')}

JOB DESCRIPTION CONTEXT:
{session.get('job_description') or 'General software engineering requirements'}

CANDIDATE RESUME HIGHLIGHTS:
{session.get('resume_summary') or 'None provided'}

CURRENT TURN / STAGE: {session['stage']} of {total_stages}

CONVERSATION HISTORY:
{conversation_log}

Candidate just said: "{effective_text}"

INSTRUCTIONS:
1. Briefly acknowledge their response naturally (1 short phrase).
2. Ask ONE concise next question calibrated for a {session['level']} candidate.
3. If they discussed a relevant project or skill, ask a thoughtful follow-up.
4. Conclude the interview if at least {total_stages} questions have been answered.
Respond with JSON containing 'acknowledgement', 'question', and 'is_complete'.
"""

                full_reply = None
                gemini_complete = False

                candidate_models = [DEFAULT_MODEL, "gemini-3.5-flash", "gemini-3.5-flash-lite"]
                for m in candidate_models:
                    try:
                        response = self.client.models.generate_content(
                            model=m,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                response_mime_type="application/json",
                                temperature=0.6,
                            ),
                        )
                        raw_text = response.text.strip()
                        data = json.loads(raw_text)
                        ack = data.get("acknowledgement", "").strip()
                        q = data.get("question", "").strip()
                        gemini_complete = bool(data.get("is_complete", False))

                        if ack and q:
                            full_reply = f"{ack} {q}"
                        else:
                            full_reply = q or ack

                        if full_reply:
                            break
                    except Exception as e:
                        print(f"Gemini generation notice with {m}: {e}")
                        continue

                if not full_reply:
                    full_reply = "Thank you for explaining that. Could you tell me more about how you structure, secure, and test your applications?"

                if on_status:
                    on_status("synthesizing_speech", "Synthesizing interviewer voice...")

                audio_b64, lipsync = synthesize_speech_with_lipsync(full_reply)

                interviewer_turn = {"role": "interviewer", "text": full_reply}
                session["history"].append(interviewer_turn)

                if db_session:
                    try:
                        from models import db
                        db_session.stage = session["stage"]
                        db_session.transcript = list(session["history"])
                        db.session.commit()
                    except Exception as e:
                        print(f"Error updating DB session: {e}")

                session["state"] = InterviewState.INTERVIEWER_SPEAKING
                session["is_processing"] = False

                result = {
                    "session_id": session_id,
                    "state": InterviewState.INTERVIEWER_SPEAKING,
                    "stage": session["stage"],
                    "total_stages": total_stages,
                    "answered_stages": session["answered_stages"],
                    "candidate_text": effective_text,
                    "text": full_reply,
                    "audio": audio_b64,
                    "lipsync": lipsync,
                    "is_complete": False,
                }
                session["last_interviewer_message"] = result
                return result

        except Exception as e:
            print(f"Error in process_candidate_speech for session {session_id}: {e}")
            session = self.sessions.get(session_id)
            if session:
                session["is_processing"] = False
                session["state"] = InterviewState.CANDIDATE_LISTENING
            return {
                "error": "Failed to process candidate response. Please try again.",
                "code": "PROCESSING_ERROR",
                "recoverable": True,
            }
        finally:
            lock.release()

    def process_candidate_response(self, session_id: str, candidate_text: str):
        """Backwards-compatible wrapper for candidate text answer."""
        return self.process_candidate_speech(session_id=session_id, candidate_text=candidate_text)

    def process_candidate_audio(self, session_id: str, audio_bytes: bytes, mime_type: str = "audio/webm"):
        """Backwards-compatible wrapper for candidate audio answer."""
        return self.process_candidate_speech(session_id=session_id, audio_bytes=audio_bytes, mime_type=mime_type)

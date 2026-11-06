import os
import base64
import threading
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, join_room

from common.tts import synthesize_speech_with_lipsync
from common.interviewer import InterviewManager, InterviewState
from models import db
from auth.controller.auth_controller import auth_blueprint
from jobs.controller.jobs_controller import jobs_blueprint
from candidates.controller.candidates_controller import candidates_blueprint
from invite.controller.invite_controller import invite_blueprint
from interview.controller.interview_controller import interview_blueprint
from roleplay.controller.roleplay_controller import roleplay_blueprint
from common.roleplay_manager import RolePlayManager, RolePlayState
from auth.service.auth_service import seed_default_organization, seed_super_admin

load_dotenv()


def get_db_uri():
    uri = os.getenv("DATABASE_URL") or os.getenv("DATABASE") or "sqlite:///interview.db"
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    if "sslmode=enable" in uri:
        uri = uri.replace("sslmode=enable", "sslmode=disable")
    return uri


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "interview-secret-key-123")
    app.config["SQLALCHEMY_DATABASE_URI"] = get_db_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    # Register API Blueprints (structured like speaking-api)
    app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
    app.register_blueprint(jobs_blueprint, url_prefix="/api/jobs")
    app.register_blueprint(candidates_blueprint, url_prefix="/api/candidates")
    app.register_blueprint(invite_blueprint, url_prefix="/api/invite")
    app.register_blueprint(interview_blueprint, url_prefix="/api/interview")
    app.register_blueprint(roleplay_blueprint, url_prefix="/api/roleplay")

    # Optional seeders for main organization & super admin (run only if table exists)
    with app.app_context():
        try:
            seed_default_organization()
            seed_super_admin()
        except Exception:
            pass

    return app


app = create_app()


@app.cli.command("seed-super-admin")
def cli_seed_super_admin():
    """Seed or update the super admin user."""
    user = seed_super_admin()
    if user:
        role_val = user.role.value if hasattr(user.role, "value") else str(user.role)
        print(f"✅ Super Admin ready: {user.email} (role: {role_val})")
    else:
        print("Failed to seed super admin.")


@app.cli.command("seed-questions")
def cli_seed_questions():
    """Seed default interview and role-play questions."""
    from seed_questions import seed_questions
    records = seed_questions()
    if records:
        print(f"✅ Done: Seeded {len(records)} question(s).")
    else:
        print("❌ Failed to seed questions.")


socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading",
    ping_timeout=120,
    ping_interval=25,
    max_http_buffer_size=20 * 1024 * 1024,
)

interview_manager = InterviewManager()
roleplay_manager = RolePlayManager()


# ──────────────────────────────── HEALTH & STANDALONE TTS ────────────────────────────────
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "interview-api",
        "ai_model": "gemini-2.5-flash",
        "voice_model": "kokoro-v1.0-timed (bm_george)"
    }), 200


@app.route("/tts", methods=["POST"])
def tts_endpoint():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Field 'text' is required"}), 400

    audio_b64, lipsync = synthesize_speech_with_lipsync(text)
    if not audio_b64:
        return jsonify({"error": "TTS synthesis failed"}), 500

    return jsonify({"audio": audio_b64, "lipsync": lipsync, "text": text}), 200


@app.route("/api/resume/parse", methods=["POST"])
def api_parse_resume():
    """Upload and parse a CV / resume file into text."""
    if "resume" not in request.files and "file" not in request.files:
        return jsonify({"error": "No file uploaded. Please upload a file with field name 'resume' or 'file'"}), 400

    file = request.files.get("resume") or request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "Invalid or empty file uploaded"}), 400

    filename = file.filename
    file_bytes = file.read()
    if not file_bytes:
        return jsonify({"error": "Uploaded file is empty"}), 400

    parsed_text = interview_manager.parse_resume(file_bytes, filename)
    if not parsed_text:
        return jsonify({"error": "Could not extract readable text from the provided file."}), 422

    return jsonify({
        "success": True,
        "filename": filename,
        "resume_text": parsed_text,
    }), 200


# ──────────────────────────────── SOCKET.IO EVENTS ────────────────────────────────
@socketio.on("connect")
def on_connect(auth=None):
    sid = getattr(request, "sid", "unknown")
    print(f" Client connected to interview-api (sid: {sid})")
    emit("bot_message", {"message": "Connected to interview voice AI."})


@socketio.on("join")
def on_join(data):
    session_id = (data or {}).get("session_id") or (data or {}).get("user_id") or "default_session"
    join_room(session_id)
    print(f" Client joined room: {session_id}")

    state_info = interview_manager.get_session_state(session_id)

    # Room confirmation
    emit("joined", {
        "session_id": session_id,
        "state": state_info["state"],
        "stage": state_info["stage"],
        "total_stages": state_info["total_stages"],
        "answered_stages": state_info["answered_stages"],
        "role": state_info.get("role"),
        "level": state_info.get("level"),
        "company": state_info.get("company"),
        "candidate_name": state_info.get("candidate_name"),
        "job_description": state_info.get("job_description"),
    })

    # Authoritative initial state
    emit("interview_state", {
        "session_id": session_id,
        "state": state_info["state"],
        "stage": state_info["stage"],
        "total_stages": state_info["total_stages"],
        "answered_stages": state_info["answered_stages"],
        "role": state_info.get("role"),
        "level": state_info.get("level"),
        "company": state_info.get("company"),
        "candidate_name": state_info.get("candidate_name"),
        "job_description": state_info.get("job_description"),
    })

    # If reconnecting to an active or completed interview, restore last interviewer turn
    if state_info.get("last_message"):
        emit("interviewer_message", state_info["last_message"])

    if state_info.get("is_complete"):
        emit("interview_completed", {
            "session_id": session_id,
            "state": "completed",
            "message": "Your interview has been completed.",
            "total_stages": state_info["total_stages"],
            "answered_stages": state_info["answered_stages"],
        })


@socketio.on("start_interview")
def on_start_interview(data):
    session_id = (data or {}).get("session_id", "default_session")
    join_room(session_id)
    role = (data or {}).get("role")
    level = (data or {}).get("level")
    total_stages = (data or {}).get("total_stages")
    candidate_name = (data or {}).get("candidate_name") or (data or {}).get("full_name")

    result = interview_manager.start_interview(
        session_id=session_id,
        role=role,
        level=level,
        total_stages=total_stages,
        candidate_name=candidate_name,
    )

    # Authoritative state change to interviewer_speaking (or completed if already finished)
    emit("interview_state", {
        "session_id": session_id,
        "state": result.get("state", "interviewer_speaking"),
        "stage": result.get("stage", 1),
        "total_stages": result.get("total_stages", 5),
        "answered_stages": result.get("answered_stages", 0),
        "role": result.get("role"),
        "level": result.get("level"),
        "company": result.get("company"),
        "candidate_name": result.get("candidate_name"),
    }, to=session_id)

    emit("interviewer_message", result, to=session_id)

    if result.get("is_complete"):
        emit("interview_completed", {
            "session_id": session_id,
            "state": "completed",
            "message": result.get("message", "Your interview has been completed."),
            "total_stages": result.get("total_stages", 5),
            "answered_stages": result.get("answered_stages", 0),
            "scorecard": result.get("scorecard"),
        }, to=session_id)


@socketio.on("playback_finished")
def on_playback_finished(data=None):
    """Notifies backend that interviewer audio finished playing, ready for candidate response."""
    session_id = (data or {}).get("session_id", "default_session") if isinstance(data, dict) else "default_session"
    state_info = interview_manager.set_candidate_turn(session_id)

    emit("interview_state", {
        "session_id": session_id,
        "state": state_info["state"],
        "stage": state_info["stage"],
        "total_stages": state_info["total_stages"],
        "answered_stages": state_info["answered_stages"],
        "role": state_info.get("role"),
        "level": state_info.get("level"),
        "company": state_info.get("company"),
        "candidate_name": state_info.get("candidate_name"),
        "job_description": state_info.get("job_description"),
    }, to=session_id)

    emit("candidate_turn", {
        "session_id": session_id,
        "stage": state_info["stage"],
        "can_speak": True,
    }, to=session_id)


@socketio.on("candidate_ready")
def on_candidate_ready(data=None):
    """Alias for playback_finished."""
    on_playback_finished(data)


@socketio.on("get_interview_state")
def on_get_interview_state(data=None):
    """Explicit client state recovery endpoint."""
    session_id = (data or {}).get("session_id", "default_session") if isinstance(data, dict) else "default_session"
    state_info = interview_manager.get_session_state(session_id)

    emit("interview_state", {
        "session_id": session_id,
        "state": state_info["state"],
        "stage": state_info["stage"],
        "total_stages": state_info["total_stages"],
        "answered_stages": state_info["answered_stages"],
    }, to=session_id)

    if state_info.get("last_message"):
        emit("interviewer_message", state_info["last_message"], to=session_id)


@socketio.on("candidate_speech")
def on_candidate_speech(data):
    """
    Candidate sends either audio bytes/base64 or text.
    Transcribes with Gemini, formulates next question or completes interview, and Kokoro speaks it.
    """
    session_id = (data or {}).get("session_id", "default_session") if isinstance(data, dict) else "default_session"
    join_room(session_id)
    raw_audio = (data or {}).get("audio") if isinstance(data, dict) else None
    text = (data or {}).get("text", "").strip() if isinstance(data, dict) else ""
    mime_type = (data or {}).get("mime_type", "audio/webm") if isinstance(data, dict) else "audio/webm"

    # 1. Reject if already completed
    if interview_manager.is_completed(session_id):
        emit("error", {
            "session_id": session_id,
            "code": "SESSION_COMPLETED",
            "error": "Interview has already been completed.",
            "recoverable": False,
        })
        return

    # 2. Reject concurrent submissions
    if interview_manager.is_processing(session_id):
        emit("error", {
            "session_id": session_id,
            "code": "CONCURRENT_PROCESSING",
            "error": "An answer is currently being processed. Please wait.",
            "recoverable": True,
        })
        return

    # 3. Decode audio if provided
    audio_bytes = None
    if raw_audio:
        try:
            if isinstance(raw_audio, str):
                if "," in raw_audio:
                    raw_audio = raw_audio.split(",", 1)[1]
                audio_bytes = base64.b64decode(raw_audio)
            else:
                audio_bytes = bytes(raw_audio)
        except Exception as e:
            emit("error", {
                "session_id": session_id,
                "code": "INVALID_AUDIO",
                "error": f"Invalid audio encoding: {e}",
                "recoverable": True,
            })
            return
    elif not text:
        emit("error", {
            "session_id": session_id,
            "code": "MISSING_INPUT",
            "error": "Missing candidate audio or text",
            "recoverable": True,
        })
        return

    # 4. Notify state transition: processing_answer
    curr_state = interview_manager.get_session_state(session_id)
    emit("interview_state", {
        "session_id": session_id,
        "state": "processing_answer",
        "stage": curr_state["stage"],
        "total_stages": curr_state["total_stages"],
        "answered_stages": curr_state["answered_stages"],
    }, to=session_id)

    def on_status(status, message=None):
        emit("processing_status", {
            "session_id": session_id,
            "status": status,
            "message": message or status,
        }, to=session_id)

    def on_transcript(transcript_text):
        emit("candidate_transcript", {
            "session_id": session_id,
            "text": transcript_text,
        }, to=session_id)

    result = interview_manager.process_candidate_speech(
        session_id=session_id,
        audio_bytes=audio_bytes,
        candidate_text=text,
        mime_type=mime_type,
        on_status=on_status,
        on_transcript=on_transcript,
    )

    if "error" in result and not result.get("text"):
        recov_state = interview_manager.get_session_state(session_id)
        emit("interview_state", {
            "session_id": session_id,
            "state": "candidate_listening",
            "stage": recov_state["stage"],
            "total_stages": recov_state["total_stages"],
            "answered_stages": recov_state["answered_stages"],
        }, to=session_id)
        emit("error", {
            "session_id": session_id,
            "code": result.get("code", "PROCESSING_ERROR"),
            "error": result.get("error", "Failed to process candidate response"),
            "recoverable": result.get("recoverable", True),
        })
        return

    # If candidate entered text directly, emit transcript for UI consistency
    if text and result.get("candidate_text"):
        emit("candidate_transcript", {
            "session_id": session_id,
            "text": result["candidate_text"],
        }, to=session_id)

    # Deliver interviewer question or farewell
    emit("interviewer_message", result, to=session_id)

    if result.get("is_complete"):
        emit("interview_state", {
            "session_id": session_id,
            "state": "completed",
            "stage": result["stage"],
            "total_stages": result["total_stages"],
            "answered_stages": result["answered_stages"],
        }, to=session_id)
        emit("interview_completed", {
            "session_id": session_id,
            "state": "completed",
            "message": result.get("message", "Your interview has been completed."),
            "total_stages": result["total_stages"],
            "answered_stages": result["answered_stages"],
            "scorecard": result.get("scorecard"),
        }, to=session_id)
    else:
        emit("interview_state", {
            "session_id": session_id,
            "state": "interviewer_speaking",
            "stage": result["stage"],
            "total_stages": result["total_stages"],
            "answered_stages": result["answered_stages"],
        }, to=session_id)


# ──────────────────────────────── ROLE-PLAY WEBSOCKET EVENTS ────────────────────────────────
@socketio.on("start_roleplay")
def on_start_roleplay(data):
    session_id = (data or {}).get("session_id", "default_roleplay")
    question_id = (data or {}).get("question_id")
    with_intro = (data or {}).get("with_intro", False)
    candidate_name = (data or {}).get("candidate_name") or (data or {}).get("full_name")
    if (data or {}).get("skip_intro"):
        with_intro = False
    join_room(session_id)
    print(f"🎭 start_roleplay: session_id={session_id}, question_id={question_id}, with_intro={with_intro}")

    result = roleplay_manager.start_roleplay(
        session_id=session_id,
        question_id=question_id,
        with_intro=with_intro,
        candidate_name=candidate_name,
    )
    result["patient_text"] = result.get("text")

    emit("roleplay_state", {
        "session_id": session_id,
        "state": result.get("state"),
        "phase": result.get("phase", "roleplay"),
        "role": result.get("role", "patient"),
        "turn_count": result.get("turn_count", 1),
        "emotional_state": result.get("emotional_state", "anxious"),
        "preparation_time": result.get("preparation_time", 180),
        "speaking_time": result.get("speaking_time", 300),
    }, to=session_id)

    # Emit under multiple compatible event names
    emit("patient_message", result, to=session_id)
    emit("roleplay_started", result, to=session_id)
    emit("patient_speech", result, to=session_id)
    if result.get("phase") == "interlocutor_intro":
        emit("interlocutor_intro", result, to=session_id)


@socketio.on("start_oet_intro")
def on_start_oet_intro(data):
    session_id = (data or {}).get("session_id", "default_roleplay")
    question_id = (data or {}).get("question_id")
    candidate_name = (data or {}).get("candidate_name") or (data or {}).get("full_name")
    join_room(session_id)
    print(f"🎙️ start_oet_intro: session_id={session_id}, question_id={question_id}")

    result = roleplay_manager.start_oet_intro(
        session_id=session_id,
        question_id=question_id,
        candidate_name=candidate_name,
    )
    emit("roleplay_state", {
        "session_id": session_id,
        "state": result.get("state"),
        "phase": "interlocutor_intro",
        "role": "interlocutor",
        "preparation_time": 180,
        "speaking_time": 300,
    }, to=session_id)
    emit("interlocutor_intro", result, to=session_id)


@socketio.on("preparation_completed")
def on_preparation_completed(data):
    session_id = (data or {}).get("session_id", "default_roleplay")
    question_id = (data or {}).get("question_id")
    join_room(session_id)
    print(f"⏱️ preparation_completed / handover: session_id={session_id}")

    result = roleplay_manager.start_handover(session_id=session_id, question_id=question_id)

    emit("roleplay_state", {
        "session_id": session_id,
        "state": "doctor_turn",
        "phase": "handover",
        "role": "interlocutor",
        "doctor_starts": True,
        "speaking_time": 300,
        "duration": 300,
    }, to=session_id)

    # Emit handover speech
    emit("roleplay_handover", result, to=session_id)


@socketio.on("start_handover")
def on_start_handover(data):
    on_preparation_completed(data)


@socketio.on("start_consultation")
def on_start_consultation(data):
    session_id = (data or {}).get("session_id", "default_roleplay")
    question_id = (data or {}).get("question_id")
    join_room(session_id)
    print(f"🩺 start_consultation: session_id={session_id}")

    result = roleplay_manager.start_consultation(session_id=session_id, question_id=question_id)
    result["patient_text"] = result.get("text")

    emit("roleplay_state", {
        "session_id": session_id,
        "state": result.get("state", "patient_speaking"),
        "phase": "roleplay",
        "role": "patient",
        "turn_count": 1,
        "emotional_state": result.get("emotional_state", "anxious"),
    }, to=session_id)
    emit("consultation_started", result, to=session_id)


@socketio.on("doctor_speech")
def on_doctor_speech(data):
    session_id = (data or {}).get("session_id", "default_roleplay")
    join_room(session_id)
    raw_b64 = (data or {}).get("audio")
    text = (data or {}).get("text")
    mime_type = (data or {}).get("mime_type", "audio/webm")
    print(f"🩺 doctor_speech: session_id={session_id}, text={text}")

    audio_bytes = None
    if raw_b64:
        try:
            if "," in raw_b64:
                raw_b64 = raw_b64.split(",", 1)[1]
            audio_bytes = base64.b64decode(raw_b64)
        except Exception as e:
            emit("error", {"session_id": session_id, "error": f"Invalid base64 audio: {e}"}, to=session_id)
            return

    emit("roleplay_state", {
        "session_id": session_id,
        "state": "processing_speech",
    }, to=session_id)

    def on_status(status, message):
        emit("processing_status", {"session_id": session_id, "status": status, "message": message}, to=session_id)

    def on_transcript(transcript_text):
        emit("doctor_transcript", {"session_id": session_id, "text": transcript_text}, to=session_id)

    result = roleplay_manager.process_doctor_speech(
        session_id=session_id,
        audio_bytes=audio_bytes,
        doctor_text=text,
        mime_type=mime_type,
        on_status=on_status,
        on_transcript=on_transcript,
    )

    if "error" in result and not result.get("text"):
        emit("error", {"session_id": session_id, "error": result.get("error")}, to=session_id)
        return

    result["patient_text"] = result.get("text")

    if text and result.get("doctor_text"):
        emit("doctor_transcript", {"session_id": session_id, "text": result["doctor_text"]}, to=session_id)

    emit("patient_speech", result, to=session_id)
    emit("roleplay_state", {
        "session_id": session_id,
        "state": result.get("state", "patient_speaking"),
        "turn_count": result.get("turn_count", 1),
        "emotional_state": result.get("emotional_state", "anxious"),
    }, to=session_id)


@socketio.on("finish_roleplay")
def on_finish_roleplay(data):
    session_id = (data or {}).get("session_id", "default_roleplay")
    auto_eval = (data or {}).get("auto_evaluate", True)
    join_room(session_id)
    print(f"🛑 finish_roleplay / time up: session_id={session_id}")

    result = roleplay_manager.finish_roleplay(session_id=session_id)

    # 1. Broadcast concluding message with TTS audio + lip-sync
    emit("roleplay_finished", result, to=session_id)
    emit("consultation_finished", result, to=session_id)
    emit("interlocutor_conclusion", result, to=session_id)
    emit("roleplay_state", {
        "session_id": session_id,
        "state": result.get("state", "completed"),
        "phase": "finished",
        "is_complete": True,
    }, to=session_id)

    # 2. Emit the analyzing event once conclusion is spoken / role-play finished
    analyzing_payload = {
        "session_id": session_id,
        "state": "analyzing",
        "status": "analyzing",
        "phase": "analyzing",
        "message": "Analyzing clinical communication and generating OET scorecard...",
    }
    emit("analyzing", analyzing_payload, to=session_id)
    emit("roleplay_analyzing", analyzing_payload, to=session_id)

    # 3. Automatically run background evaluation if enabled so results arrive seamlessly
    if auto_eval:
        def _bg_eval():
            try:
                with app.app_context():
                    eval_result = roleplay_manager.evaluate_roleplay(session_id=session_id)
                    socketio.emit("roleplay_completed", eval_result, to=session_id)
                    socketio.emit("roleplay_evaluated", eval_result, to=session_id)
                    socketio.emit("roleplay_state", {
                        "session_id": session_id,
                        "state": "completed",
                        "phase": "completed",
                        "is_complete": True,
                    }, to=session_id)
            except Exception as e:
                print(f"Background evaluation notice for {session_id}: {e}")

        threading.Thread(target=_bg_eval, daemon=True).start()


@socketio.on("roleplay_time_up")
def on_roleplay_time_up(data):
    on_finish_roleplay(data)


@socketio.on("time_up")
def on_time_up(data):
    on_finish_roleplay(data)


@socketio.on("stop_roleplay")
def on_stop_roleplay(data):
    on_finish_roleplay(data)


@socketio.on("analyzing")
def on_analyzing(data):
    """Explicit client trigger to show analyzing state and receive scorecard."""
    session_id = (data or {}).get("session_id", "default_roleplay")
    join_room(session_id)
    emit("analyzing", {
        "session_id": session_id,
        "state": "analyzing",
        "status": "analyzing",
        "phase": "analyzing",
        "message": "Analyzing clinical communication and generating OET scorecard...",
    }, to=session_id)
    result = roleplay_manager.evaluate_roleplay(session_id=session_id)
    emit("roleplay_completed", result, to=session_id)
    emit("roleplay_evaluated", result, to=session_id)


@socketio.on("start_analyzing")
def on_start_analyzing(data):
    on_analyzing(data)


@socketio.on("evaluate_roleplay")
def on_evaluate_roleplay(data):
    session_id = (data or {}).get("session_id", "default_roleplay")
    join_room(session_id)
    print(f"📋 evaluate_roleplay: session_id={session_id}")
    analyzing_payload = {
        "session_id": session_id,
        "state": "analyzing",
        "status": "analyzing",
        "phase": "analyzing",
        "message": "Analyzing clinical communication and generating OET scorecard...",
    }
    emit("analyzing", analyzing_payload, to=session_id)
    emit("roleplay_analyzing", analyzing_payload, to=session_id)
    emit("roleplay_state", analyzing_payload, to=session_id)

    result = roleplay_manager.evaluate_roleplay(session_id=session_id)
    emit("roleplay_completed", result, to=session_id)
    emit("roleplay_evaluated", result, to=session_id)
    emit("roleplay_state", {
        "session_id": session_id,
        "state": "completed",
        "phase": "completed",
        "is_complete": True,
    }, to=session_id)


@socketio.on("speak")
def on_speak(data):
    """Simple raw TTS synthesis event."""
    text = data.get("text", "").strip() if isinstance(data, dict) else ""
    user_id = data.get("user_id") if isinstance(data, dict) else None

    if not text:
        emit("error", {"error": "Text is empty"})
        return

    audio_b64, lipsync = synthesize_speech_with_lipsync(text)
    response_data = {"message": text, "audio": audio_b64, "lipsync": lipsync}

    if user_id:
        emit("bot_message", response_data, to=user_id)
    else:
        emit("bot_message", response_data)


@socketio.on("ping")
def handle_ping():
    emit("pong")


@socketio.on("disconnect")
def on_disconnect(*args):
    reason = args[0] if args else "unknown"
    sid = getattr(request, "sid", "unknown")
    print(f" Client disconnected (sid: {sid}, reason: {reason})")


if __name__ == "__main__":
    DEBUG_MODE = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")

    # Pre-warm voice model on startup (warm up Ready, static OET intro, handover, and conclusion)
    def _warmup_tts():
        try:
            synthesize_speech_with_lipsync("Ready.")
            synthesize_speech_with_lipsync(roleplay_manager.build_oet_intro())
            synthesize_speech_with_lipsync(roleplay_manager.build_interlocutor_handover())
            synthesize_speech_with_lipsync(roleplay_manager.build_interlocutor_conclusion())
            print("🔊 Kokoro voice model pre-warmed (Ready + OET Intro + Handover + Conclusion).")
        except Exception as e:
            print(f"Voice model warmup notice: {e}")

    if not DEBUG_MODE or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(
            target=_warmup_tts,
            daemon=True,
        ).start()

    port = int(os.getenv("PORT", 5002))
    print(f"Starting interview-api (Gemini + Kokoro TTS) on port {port}...")
    socketio.run(
        app,
        host="0.0.0.0",
        port=port,
        debug=DEBUG_MODE,
        use_debugger=False,
        use_reloader=DEBUG_MODE,
        allow_unsafe_werkzeug=True,
    )

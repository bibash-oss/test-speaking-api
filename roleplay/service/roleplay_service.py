from common.roleplay_manager import RolePlayManager

roleplay_manager = RolePlayManager()


def start_roleplay_service(dto):
    return roleplay_manager.start_roleplay(
        session_id=dto.session_id,
        question_id=dto.question_id,
        with_intro=getattr(dto, "with_intro", False),
    )


def start_oet_intro_service(session_id: str, question_id: str = None):
    return roleplay_manager.start_oet_intro(session_id=session_id, question_id=question_id)


def start_consultation_service(session_id: str, question_id: str = None):
    return roleplay_manager.start_consultation(session_id=session_id, question_id=question_id)


def start_handover_service(session_id: str, question_id: str = None):
    return roleplay_manager.start_handover(session_id=session_id, question_id=question_id)


def finish_roleplay_service(session_id: str):
    return roleplay_manager.finish_roleplay(session_id=session_id)


def process_doctor_speech_service(dto):
    return roleplay_manager.process_doctor_speech(
        session_id=dto.session_id,
        audio_bytes=dto.audio_bytes,
        doctor_text=dto.text,
        mime_type=dto.mime_type,
    )


def evaluate_roleplay_service(session_id: str):
    return roleplay_manager.evaluate_roleplay(session_id=session_id)


def get_roleplay_state_service(session_id: str):
    session = roleplay_manager.get_or_create_session(session_id)
    return {
        "session_id": session_id,
        "state": session.get("state"),
        "turn_count": session.get("turn_count", 0),
        "question": session.get("question"),
        "is_complete": session.get("state") == "completed",
        "last_message": session.get("last_patient_message"),
        "scorecard": session.get("scorecard"),
    }


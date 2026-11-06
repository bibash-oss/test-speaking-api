from common.interviewer import InterviewManager

interview_manager = InterviewManager()


def start_interview_service(dto):
    return interview_manager.start_interview(
        session_id=dto.session_id,
        role=dto.role,
        level=dto.level,
        total_stages=dto.total_stages,
    )


def respond_interview_service(dto):
    return interview_manager.process_candidate_speech(
        session_id=dto.session_id,
        audio_bytes=dto.audio_bytes,
        candidate_text=dto.text,
        mime_type=dto.mime_type,
    )


def get_interview_state_service(session_id: str):
    return interview_manager.get_session_state(session_id)


def parse_resume_service(file_bytes: bytes, filename: str):
    return interview_manager.parse_resume(file_bytes, filename)


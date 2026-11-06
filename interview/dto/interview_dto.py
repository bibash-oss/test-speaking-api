import base64


class StartInterviewDTO:
    def __init__(self, session_id: str, role: str = None, level: str = None, total_stages: int = None):
        self.session_id = session_id or "default_session"
        self.role = role
        self.level = level
        self.total_stages = int(total_stages) if total_stages else None

    @staticmethod
    def from_dict(data: dict):
        d = data or {}
        return StartInterviewDTO(
            session_id=d.get("session_id", "default_session"),
            role=d.get("role"),
            level=d.get("level"),
            total_stages=d.get("total_stages"),
        )


class RespondInterviewDTO:
    def __init__(self, session_id: str, text: str = None, audio_bytes: bytes = None, mime_type: str = "audio/webm"):
        self.session_id = session_id or "default_session"
        self.text = text
        self.audio_bytes = audio_bytes
        self.mime_type = mime_type

    @staticmethod
    def from_request(req):
        session_id = "default_session"
        candidate_text = None
        audio_bytes = None
        mime_type = "audio/webm"

        if req.is_json:
            data = req.get_json() or {}
            session_id = data.get("session_id", "default_session")
            candidate_text = data.get("text", "").strip() or None
            raw_b64 = data.get("audio")
            mime_type = data.get("mime_type", "audio/webm")
            if raw_b64:
                if "," in raw_b64:
                    raw_b64 = raw_b64.split(",", 1)[1]
                audio_bytes = base64.b64decode(raw_b64)
        else:
            session_id = req.form.get("session_id", "default_session")
            candidate_text = req.form.get("text", "").strip() or None
            mime_type = req.form.get("mime_type", "audio/webm")

            if "audio" in req.files:
                file = req.files["audio"]
                audio_bytes = file.read()
                if file.content_type:
                    mime_type = file.content_type

        return RespondInterviewDTO(
            session_id=session_id,
            text=candidate_text,
            audio_bytes=audio_bytes,
            mime_type=mime_type,
        )


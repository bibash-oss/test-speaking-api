import base64


class StartRolePlayDTO:
    def __init__(self, session_id: str = None, question_id: str = None, with_intro: bool = False):
        self.session_id = session_id or "default_roleplay"
        self.question_id = question_id
        self.with_intro = with_intro

    @staticmethod
    def from_dict(data: dict):
        d = data or {}
        return StartRolePlayDTO(
            session_id=d.get("session_id", "default_roleplay"),
            question_id=d.get("question_id"),
            with_intro=d.get("with_intro", False),
        )


class DoctorSpeechDTO:
    def __init__(self, session_id: str, text: str = None, audio_bytes: bytes = None, mime_type: str = "audio/webm"):
        self.session_id = session_id or "default_roleplay"
        self.text = text
        self.audio_bytes = audio_bytes
        self.mime_type = mime_type

    @staticmethod
    def from_request(req):
        session_id = "default_roleplay"
        doctor_text = None
        audio_bytes = None
        mime_type = "audio/webm"

        if req.is_json:
            data = req.get_json() or {}
            session_id = data.get("session_id", "default_roleplay")
            doctor_text = data.get("text", "").strip() or None
            raw_b64 = data.get("audio")
            mime_type = data.get("mime_type", "audio/webm")
            if raw_b64:
                if "," in raw_b64:
                    raw_b64 = raw_b64.split(",", 1)[1]
                audio_bytes = base64.b64decode(raw_b64)
        else:
            session_id = req.form.get("session_id", "default_roleplay")
            doctor_text = req.form.get("text", "").strip() or None
            mime_type = req.form.get("mime_type", "audio/webm")

            if "audio" in req.files:
                file = req.files["audio"]
                audio_bytes = file.read()
                if file.content_type:
                    mime_type = file.content_type

        return DoctorSpeechDTO(
            session_id=session_id,
            text=doctor_text,
            audio_bytes=audio_bytes,
            mime_type=mime_type,
        )


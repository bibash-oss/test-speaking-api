class RegisterCandidateDTO:
    def __init__(
        self,
        full_name: str,
        email: str,
        phone: str = "",
        resume_text: str = "",
        resume_filename: str = "",
        resume_bytes: bytes = None,
        role: str = "",
        level: str = "",
        job_id: str = "",
    ):
        self.full_name = full_name.strip() if full_name else ""
        self.email = email.strip().lower() if email else ""
        self.phone = phone.strip() if phone else ""
        self.resume_text = resume_text.strip() if resume_text else ""
        self.resume_filename = resume_filename.strip() if resume_filename else ""
        self.resume_bytes = resume_bytes
        self.role = role.strip() if role else ""
        self.position = self.role

        detected_level = level.strip() if level else ""
        if not detected_level and self.role:
            r_low = self.role.lower()
            if "intern" in r_low:
                detected_level = "Intern"
            elif "junior" in r_low:
                detected_level = "Junior"
            elif "senior" in r_low:
                detected_level = "Senior"
            elif "lead" in r_low:
                detected_level = "Lead"

        self.level = detected_level
        self.job_id = job_id.strip() if job_id else ""

    @staticmethod
    def from_request(req):
        if req.is_json:
            data = req.get_json() or {}
            full_name = data.get("full_name", "").strip()
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            role = (
                data.get("position")
                or data.get("role")
                or data.get("job_title")
                or data.get("title")
                or data.get("applied_for")
                or data.get("applied_role")
                or ""
            ).strip()
            level = (
                data.get("level")
                or data.get("seniority")
                or data.get("experience_level")
                or data.get("job_level")
                or ""
            ).strip()
            job_id = (data.get("job_id") or data.get("jobId") or "").strip()
            resume_text = data.get("resume_text", "").strip()
            resume_filename = ""
            resume_bytes = None
        else:
            full_name = req.form.get("full_name", "").strip()
            email = req.form.get("email", "").strip()
            phone = req.form.get("phone", "").strip()
            role = (
                req.form.get("position")
                or req.form.get("role")
                or req.form.get("job_title")
                or req.form.get("title")
                or req.form.get("applied_for")
                or req.form.get("applied_role")
                or ""
            ).strip()
            level = (
                req.form.get("level")
                or req.form.get("seniority")
                or req.form.get("experience_level")
                or req.form.get("job_level")
                or ""
            ).strip()
            job_id = (req.form.get("job_id") or req.form.get("jobId") or "").strip()
            resume_text = req.form.get("resume_text", "").strip()
            resume_filename = ""
            resume_bytes = None

            if "resume" in req.files:
                file = req.files["resume"]
                if file and file.filename:
                    resume_filename = file.filename
                    resume_bytes = file.read()

        if not full_name:
            raise ValueError("Field 'full_name' is required")
        if not email:
            raise ValueError("Field 'email' is required")

        return RegisterCandidateDTO(
            full_name=full_name,
            email=email,
            phone=phone,
            resume_text=resume_text,
            resume_filename=resume_filename,
            resume_bytes=resume_bytes,
            role=role,
            level=level,
            job_id=job_id,
        )


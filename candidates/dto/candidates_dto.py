class CandidateResponseDTO:
    @staticmethod
    def format_candidate(candidate):
        if not candidate:
            return None
        c_dict = candidate.to_dict()
        session = candidate.interview_session
        if session:
            c_dict["interview"] = {
                "session_token": session.session_token,
                "status": session.status,
                "stage": session.stage,
                "scorecard": session.scorecard,
                "started_at": session.started_at.isoformat() if session.started_at else None,
                "completed_at": session.completed_at.isoformat() if session.completed_at else None,
            }
            c_dict["transcript"] = session.transcript or []
        else:
            c_dict["interview"] = None
            c_dict["transcript"] = []

        if candidate.job:
            c_dict["job"] = {
                "id": candidate.job.id,
                "title": candidate.job.title,
                "level": candidate.job.level,
                "company_name": candidate.job.company_name,
            }

        return c_dict


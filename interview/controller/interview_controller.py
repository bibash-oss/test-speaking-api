from flask import Blueprint, request, jsonify
from interview.dto.interview_dto import StartInterviewDTO, RespondInterviewDTO
from interview.service.interview_service import (
    start_interview_service,
    respond_interview_service,
    get_interview_state_service,
    parse_resume_service,
)

interview_blueprint = Blueprint("interview_blueprint", __name__)


@interview_blueprint.route("/start", methods=["POST"])
def api_start_interview():
    data = request.get_json(silent=True) or {}
    dto = StartInterviewDTO.from_dict(data)
    result = start_interview_service(dto)
    return jsonify(result), 200


@interview_blueprint.route("/respond", methods=["POST"])
def api_interview_respond():
    try:
        dto = RespondInterviewDTO.from_request(request)
    except Exception as e:
        return jsonify({"error": f"Invalid request: {e}"}), 400

    result = respond_interview_service(dto)
    return jsonify(result), 200


@interview_blueprint.route("/state/<session_id>", methods=["GET"])
def api_interview_state(session_id):
    state_info = get_interview_state_service(session_id)
    return jsonify(state_info), 200


@interview_blueprint.route("/parse-resume", methods=["POST"])
def api_interview_parse_resume():
    if "resume" not in request.files and "file" not in request.files:
        return jsonify({"error": "No file uploaded. Please upload a file with field name 'resume' or 'file'"}), 400

    file = request.files.get("resume") or request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "Invalid or empty file uploaded"}), 400

    file_bytes = file.read()
    if not file_bytes:
        return jsonify({"error": "Uploaded file is empty"}), 400

    parsed_text = parse_resume_service(file_bytes, file.filename)
    if not parsed_text:
        return jsonify({"error": "Could not extract readable text from the provided file."}), 422

    return jsonify({
        "success": True,
        "filename": file.filename,
        "resume_text": parsed_text,
    }), 200


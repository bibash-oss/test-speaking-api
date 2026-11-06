from flask import Blueprint, request, jsonify
from roleplay.dto.roleplay_dto import StartRolePlayDTO, DoctorSpeechDTO
from roleplay.service.roleplay_service import (
    start_roleplay_service,
    start_oet_intro_service,
    start_handover_service,
    finish_roleplay_service,
    start_consultation_service,
    process_doctor_speech_service,
    evaluate_roleplay_service,
    get_roleplay_state_service,
)

roleplay_blueprint = Blueprint("roleplay_blueprint", __name__)


@roleplay_blueprint.route("/start", methods=["POST"])
def api_start_roleplay():
    data = request.get_json(silent=True) or {}
    dto = StartRolePlayDTO.from_dict(data)
    result = start_roleplay_service(dto)
    return jsonify(result), 200


@roleplay_blueprint.route("/intro", methods=["POST"])
def api_start_oet_intro():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id", "default_roleplay")
    question_id = data.get("question_id")
    result = start_oet_intro_service(session_id, question_id)
    return jsonify(result), 200


@roleplay_blueprint.route("/handover", methods=["POST"])
def api_start_handover():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id", "default_roleplay")
    question_id = data.get("question_id")
    result = start_handover_service(session_id, question_id)
    return jsonify(result), 200


@roleplay_blueprint.route("/finish", methods=["POST"])
def api_finish_roleplay():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id", "default_roleplay")
    result = finish_roleplay_service(session_id)
    return jsonify(result), 200


@roleplay_blueprint.route("/start-consultation", methods=["POST"])
def api_start_consultation():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id", "default_roleplay")
    question_id = data.get("question_id")
    result = start_consultation_service(session_id, question_id)
    return jsonify(result), 200


@roleplay_blueprint.route("/respond", methods=["POST"])
def api_respond_roleplay():
    try:
        dto = DoctorSpeechDTO.from_request(request)
    except Exception as e:
        return jsonify({"error": f"Invalid request payload: {e}"}), 400

    result = process_doctor_speech_service(dto)
    status_code = 400 if "error" in result and not result.get("text") else 200
    return jsonify(result), status_code


@roleplay_blueprint.route("/state/<session_id>", methods=["GET"])
def api_roleplay_state(session_id):
    state_info = get_roleplay_state_service(session_id)
    return jsonify(state_info), 200


@roleplay_blueprint.route("/evaluate/<session_id>", methods=["POST"])
def api_evaluate_roleplay(session_id):
    scorecard = evaluate_roleplay_service(session_id)
    return jsonify(scorecard), 200


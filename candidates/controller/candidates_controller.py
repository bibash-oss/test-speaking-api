from flask import Blueprint, request, jsonify
from common.auth import require_auth
from candidates.service.candidates_service import (
    get_candidate_service,
    register_direct_candidate_service,
)
from invite.dto.invite_dto import RegisterCandidateDTO

candidates_blueprint = Blueprint("candidates_blueprint", __name__)


@candidates_blueprint.route("/register", methods=["POST"])
@candidates_blueprint.route("", methods=["POST"])
def register_candidate():
    """Public candidate registration endpoint without requiring an invite link."""
    try:
        dto = RegisterCandidateDTO.from_request(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    res, err, status = register_direct_candidate_service(dto)
    if err:
        return jsonify({"error": err}), status
    return jsonify(res), status


@candidates_blueprint.route("/<candidate_id>", methods=["GET"])
@require_auth
def get_candidate(candidate_id):
    candidate = get_candidate_service(candidate_id)
    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404
    return jsonify({"candidate": candidate}), 200


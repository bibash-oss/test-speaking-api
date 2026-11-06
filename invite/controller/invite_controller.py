from flask import Blueprint, request, jsonify
from invite.dto.invite_dto import RegisterCandidateDTO
from invite.service.invite_service import get_invite_info_service, register_candidate_service

invite_blueprint = Blueprint("invite_blueprint", __name__)


@invite_blueprint.route("/<token>", methods=["GET"])
def get_invite_info(token):
    res, err, status = get_invite_info_service(token)
    if err:
        return jsonify({"error": err}), status
    return jsonify(res), 200


@invite_blueprint.route("/<token>/register", methods=["POST"])
def register_candidate(token):
    try:
        dto = RegisterCandidateDTO.from_request(request)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    res, err, status = register_candidate_service(token, dto)
    if err:
        return jsonify({"error": err}), status
    return jsonify(res), status


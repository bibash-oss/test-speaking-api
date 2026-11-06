from flask import Blueprint, request, jsonify, g
from common.auth import require_auth
from auth.dto.auth_dto import LoginUserDTO
from auth.service.auth_service import login_user

auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    try:
        dto = LoginUserDTO.from_dict(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    result, err, status = login_user(dto.email, dto.password)
    if err:
        return jsonify({"error": err}), status

    return jsonify({
        "message": "Login successful",
        "token": result["token"],
        "role": result["role"],
    }), 200


@auth_blueprint.route("/me", methods=["GET"])
@require_auth
def get_current_profile():
    """Return the profile of the currently authenticated organization."""
    return jsonify({
        "organization": g.current_org.to_dict(),
    }), 200

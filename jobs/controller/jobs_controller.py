from flask import Blueprint, request, jsonify, g
from common.auth import require_auth
from jobs.dto.jobs_dto import CreateJobDTO
from jobs.service.jobs_service import (
    create_job_service,
    list_jobs_service,
    get_job_service,
    get_job_candidates_service,
)

jobs_blueprint = Blueprint("jobs_blueprint", __name__)


@jobs_blueprint.route("", methods=["POST"])
@require_auth
def create_job():
    data = request.get_json(silent=True) or {}
    try:
        dto = CreateJobDTO.from_dict(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    org_id = getattr(g, "current_org_id", None)
    org_name = g.current_org.name if hasattr(g, "current_org") and g.current_org else "Company"

    res = create_job_service(dto, org_id=org_id, org_name=org_name)
    return jsonify({"message": "Job created successfully", "job": res}), 201


@jobs_blueprint.route("", methods=["GET"])
def list_jobs():
    jobs = list_jobs_service()
    return jsonify({"jobs": jobs}), 200


@jobs_blueprint.route("/<job_id>", methods=["GET"])
def get_job(job_id):
    res = get_job_service(job_id)
    if not res:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({"job": res}), 200


@jobs_blueprint.route("/<job_id>/candidates", methods=["GET"])
@require_auth
def get_job_candidates(job_id):
    res = get_job_candidates_service(job_id)
    if not res:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(res), 200


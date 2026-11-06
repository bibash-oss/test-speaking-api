import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify, current_app, g
from models.organizations import Organization


def generate_token(org: Organization) -> str:
    """Generate a signed JWT token valid for 7 days."""
    secret_key = current_app.config.get("SECRET_KEY", "interview-secret-key-123")
    now = datetime.now(timezone.utc)
    role_val = org.role.value if hasattr(org.role, "value") else str(org.role)
    payload = {
        "org_id": org.id,
        "email": org.email,
        "fullName": org.name,
        "role": role_val,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=7)).timestamp()),
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


def require_auth(f):
    """
    Decorator to protect organization/admin endpoints.
    Expects 'Authorization: Bearer <jwt_token>' header.
    Sets g.current_org and g.current_org_id on successful authentication.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 401

        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Invalid Authorization header format. Expected 'Bearer <token>'"}), 401

        token = parts[1].strip()
        secret_key = current_app.config.get("SECRET_KEY", "interview-secret-key-123")

        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Authentication token has expired. Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid authentication token."}), 401

        org_id = payload.get("org_id")
        if not org_id:
            return jsonify({"error": "Token is missing organization identifier."}), 401

        org = Organization.query.get(org_id)
        if not org:
            return jsonify({"error": "Organization account not found."}), 401

        if not org.is_active:
            return jsonify({"error": "Organization account is inactive. Please contact support."}), 403

        # Attach organization to Flask request context
        g.current_org = org
        g.current_org_id = org.id

        return f(*args, **kwargs)

    return decorated


def require_role(*allowed_roles):
    """
    Decorator to restrict endpoints to specific roles (e.g. 'super_admin', 'admin', UserRole.SUPER_ADMIN).
    Automatically enforces require_auth first.
    """
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated(*args, **kwargs):
            role_val = g.current_org.role.value if hasattr(g.current_org.role, "value") else str(g.current_org.role)
            allowed = [r.value if hasattr(r, "value") else str(r) for r in allowed_roles]
            if role_val not in allowed:
                return jsonify({"error": "Forbidden: Insufficient privileges"}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


def require_super_admin(f):
    """
    Decorator to restrict access strictly to super_admin users.
    Automatically enforces require_auth first.
    """
    return require_role("super_admin")(f)

from flask import jsonify


def api_response(message: str, status: str, data=None, http_status: int = 200):
    """
    Universal API response format matching speaking-api
    status: "success" or "error"
    """
    response = {
        "message": message,
        "status": status,
        "data": data if data is not None else None,
    }
    return jsonify(response), http_status


# Shortcut helpers
def success(message: str = "Success", data=None, http_status: int = 200):
    return api_response(message, "success", data, http_status)


def error(message: str = "An error occurred", data=None, http_status: int = 400):
    return api_response(message, "error", data, http_status)


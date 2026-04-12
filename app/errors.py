from flask import jsonify


class ApiError(Exception):
    def __init__(self, message, status_code=400, error_code="bad_request"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)


def success_response(data=None, message="Success", status_code=200):
    response = {
        "success": True,
        "message": message,
        "data": data,
    }
    return jsonify(response), status_code


def error_response(message, status_code=400, error_code="bad_request", details=None):
    response = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
        },
    }

    if details is not None:
        response["error"]["details"] = details

    return jsonify(response), status_code
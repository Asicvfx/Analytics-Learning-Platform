"""Wrap DRF errors into the unified {success, data, message} envelope."""
from rest_framework.views import exception_handler


_DEFAULT_MESSAGES = {
    400: "Invalid request data.",
    401: "Authentication required.",
    403: "You do not have permission to perform this action.",
    404: "Resource not found.",
    500: "Something went wrong. Please try again later.",
}


def _extract_message(data, status_code):
    if isinstance(data, dict):
        if "detail" in data:
            return str(data["detail"])
        # First field error, if any.
        for value in data.values():
            if isinstance(value, (list, tuple)) and value:
                return str(value[0])
            return str(value)
    if isinstance(data, list) and data:
        return str(data[0])
    return _DEFAULT_MESSAGES.get(status_code, "Request failed.")


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None
    message = _extract_message(response.data, response.status_code)
    response.data = {"success": False, "data": None, "message": message}
    return response

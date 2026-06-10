"""Helpers for the unified API response envelope: {success, data, message}."""
from rest_framework.response import Response


def ok(data=None, message=None, status=200):
    return Response({"success": True, "data": data, "message": message}, status=status)


def fail(message, data=None, status=400):
    return Response({"success": False, "data": data, "message": message}, status=status)

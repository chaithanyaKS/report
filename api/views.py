from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["GET"])
def ping(request: Request) -> Response:
    return Response({"detail": "Service up anď running"})


@api_view(["POST"])
def get_report(request: Request) -> Response:
    return Response({"detail": "get-report"})


@api_view(["POST"])
def trigger_report(request: Request) -> Response:
    return Response({"detail": "trigger-report"})

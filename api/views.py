from datetime import datetime, timedelta

from celery import group, states
from django.http.response import StreamingHttpResponse
from django.utils.timezone import make_aware
from django_celery_results.models import ALL_STATES, TaskResult
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Report
from api.tasks import generate_report

# Assuming Jan 25th 2023 as the current day since it is latest date available in the database
CURRENT_DATE = datetime(2023, 1, 25)
LAST_HOUR = CURRENT_DATE - timedelta(hours=1)
LAST_DAY = CURRENT_DATE - timedelta(days=1)
LAST_WEEK = CURRENT_DATE - timedelta(days=7)


@api_view(["GET"])
def ping(request: Request) -> Response:
    return Response({"detail": "Service up anď running"})


@api_view(["POST"])
def get_report(request: Request) -> Response | StreamingHttpResponse:
    report_id = request.data.get("report_id")
    if report_id is None:
        return Response(
            {"detail": "report_id is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        task = TaskResult.objects.get(task_id=report_id)
        if task.status.lower() == "failure":
            return Response({"status": "failed"})
        elif task.status.lower() != "success":
            return Response({"status": "Running"})
        else:
            report = Report.objects.get(task__task_id=report_id)
            return StreamingHttpResponse(
                report.file.readlines(), content_type="text/csv"
            )
    except TaskResult.DoesNotExist:
        return Response(
            {"detail": "invalid report_id"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Report.DoesNotExist:
        return Response(
            {"detail": "invalid report_id"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
def trigger_report(request: Request) -> Response:
    task = generate_report.delay(CURRENT_DATE)
    return Response({"report_id": task.task_id})

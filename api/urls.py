from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path("ping/", views.ping, name="ping"),
    path("get_report/", views.get_report, name="get-report"),
    path("trigger_report/", views.trigger_report, name="trigger-report"),
]

from django.urls import path

from . import views

app_name = "manager"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("meetings/", views.meeting_list, name="meeting_list"),
    path(
        "meetings/<int:meeting_id>/",
        views.meeting_detail,
        name="meeting_detail",
    ),
    path(
        "meetings/<int:meeting_id>/attendance/",
        views.attendance_result,
        name="attendance_result",
    ),
    path("meetings/create/", views.meeting_create, name="meeting_create"),
]
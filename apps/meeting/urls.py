from django.urls import path

from . import views

app_name = "meeting"

urlpatterns = [
    path(
        "<int:meeting_id>/vote/",
        views.vote,
        name="vote",
    ),

    path(
        "<int:meeting_id>/result/",
        views.result,
        name="result",
    ),

    path(
        "<int:meeting_id>/attendance/",
        views.attendance,
        name="attendance",
    ),
]
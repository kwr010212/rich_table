from django.urls import path

from . import views


app_name = "manager"


urlpatterns = [
    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    # 참가자 관리
    path(
        "participants/",
        views.participant_list,
        name="participant_list",
    ),

    # 모임 목록
    path(
        "meetings/",
        views.meeting_list,
        name="meeting_list",
    ),

    # 모임 생성
    path(
        "meetings/create/",
        views.meeting_create,
        name="meeting_create",
    ),

    # 모임 상세 / 관리
    path(
        "meetings/<int:meeting_id>/",
        views.meeting_detail,
        name="meeting_detail",
    ),

    # 참석 결과
    path(
        "meetings/<int:meeting_id>/attendance/",
        views.attendance_result,
        name="attendance_result",
    ),
]
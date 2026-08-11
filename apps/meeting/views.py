from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from apps.survey.models import Participant

from .forms import (
    AvailabilityVoteForm,
    AttendanceForm,
)

from .models import (
    AvailabilityVote,
    Attendance,
    Meeting,
)


def meeting_list(request):
    meetings = Meeting.objects.filter(
        status=Meeting.Status.VOTING
    )

    return render(
        request,
        "meeting/list.html",
        {
            "meetings": meetings,
        },
    )


def vote(request, meeting_id):

    meeting = get_object_or_404(
        Meeting,
        pk=meeting_id,
    )

    participant_id = request.session.get("participant_id")

    if not participant_id:
        return redirect("survey:enter")

    participant = get_object_or_404(
        Participant,
        pk=participant_id,
    )

    if request.method == "POST":

        form = AvailabilityVoteForm(
            request.POST,
            meeting=meeting,
        )

        if form.is_valid():

            # 기존 투표 삭제
            AvailabilityVote.objects.filter(
                meeting=meeting,
                participant=participant,
            ).delete()

            # 선택한 시간 저장
            for candidate in form.cleaned_data["candidates"]:

                AvailabilityVote.objects.create(
                    meeting=meeting,
                    participant=participant,
                    weekday=candidate.weekday,
                    meal_type=candidate.meal_type,
                    is_unavailable=False,
                )

            # 시간 안됨 저장
            if form.cleaned_data["unavailable"]:

                AvailabilityVote.objects.create(
                    meeting=meeting,
                    participant=participant,
                    weekday=None,
                    meal_type=None,
                    is_unavailable=True,
                )

            return redirect("main:dashboard")

    else:

        form = AvailabilityVoteForm(
            meeting=meeting,
        )

    return render(
        request,
        "meeting/vote.html",
        {
            "meeting": meeting,
            "form": form,
        },
    )


def result(request, meeting_id):

    meeting = get_object_or_404(
        Meeting,
        pk=meeting_id,
    )

    results = (
        AvailabilityVote.objects
        .filter(
            meeting=meeting,
            is_unavailable=False,
        )
        .values("weekday", "meal_type")
        .annotate(count=Count("id"))
        .order_by(
            "weekday",
            "meal_type",
        )
    )

    weekday_map = dict(
        AvailabilityVote.Weekday.choices
    )

    meal_map = dict(
        AvailabilityVote.MealType.choices
    )

    unavailable_count = (
        AvailabilityVote.objects
        .filter(
            meeting=meeting,
            is_unavailable=True,
        )
        .count()
    )

    return render(
        request,
        "meeting/result.html",
        {
            "meeting": meeting,
            "results": results,
            "weekday_map": weekday_map,
            "meal_map": meal_map,
            "unavailable_count": unavailable_count,
        },
    )


def attendance(request, meeting_id):

    meeting = get_object_or_404(
        Meeting,
        pk=meeting_id,
    )

    # 아직 확정되지 않은 모임은 참석 투표 불가
    if meeting.status != Meeting.Status.CONFIRMED:
        return redirect("main:dashboard")

    participant_id = request.session.get("participant_id")

    if not participant_id:
        return redirect("survey:enter")

    participant = get_object_or_404(
        Participant,
        pk=participant_id,
    )

    attendance = Attendance.objects.filter(
        meeting=meeting,
        participant=participant,
    ).first()

    if request.method == "POST":

        form = AttendanceForm(request.POST)

        if form.is_valid():

            Attendance.objects.update_or_create(
                meeting=meeting,
                participant=participant,
                defaults={
                    "status": form.cleaned_data["status"],
                },
            )

            return redirect("main:dashboard")

    else:

        initial = {}

        if attendance:
            initial["status"] = attendance.status

        form = AttendanceForm(
            initial=initial
        )

    return render(
        request,
        "meeting/attendance.html",
        {
            "meeting": meeting,
            "form": form,
        },
    )
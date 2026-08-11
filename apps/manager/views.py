from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from apps.meeting.models import (
    Attendance,
    AvailabilityVote,
    Meeting,
    MeetingCandidate,
)
from apps.survey.models import Participant

from .forms import (
    MeetingConfirmForm,
    MeetingForm,
)


def dashboard(request):
    return render(
        request,
        "manager/dashboard.html",
    )


def participant_list(request):
    participants = (
        Participant.objects
        .filter(is_active=True)
        .order_by("name")
    )

    return render(
        request,
        "manager/participant_list.html",
        {
            "participants": participants,
        },
    )


def meeting_list(request):
    meetings = Meeting.objects.all()

    return render(
        request,
        "manager/meeting_list.html",
        {
            "meetings": meetings,
        },
    )


def meeting_create(request):

    if request.method == "POST":

        form = MeetingForm(request.POST)

        if form.is_valid():

            meeting = form.save()

            selected_slots = form.cleaned_data["available_slots"]

            for slot in selected_slots:

                weekday, meal_type = slot.split("_")

                MeetingCandidate.objects.create(
                    meeting=meeting,
                    weekday=weekday,
                    meal_type=meal_type,
                )

            return redirect(
                "manager:meeting_list"
            )

    else:

        form = MeetingForm()

    return render(
        request,
        "manager/meeting_create.html",
        {
            "form": form,
        },
    )

def meeting_detail(request, meeting_id):

    meeting = get_object_or_404(
        Meeting,
        pk=meeting_id,
    )

    # -----------------------------
    # 요일 투표 결과 집계
    # -----------------------------

    vote_results = (
        meeting.availability_votes
        .filter(is_unavailable=False)
        .values("weekday", "meal_type")
        .annotate(vote_count=Count("id"))
        .order_by("-vote_count", "weekday", "meal_type")
    )

    unavailable_votes = (
        meeting.availability_votes
        .filter(is_unavailable=True)
        .select_related("participant")
    )

    unavailable_count = unavailable_votes.count()

    unavailable_voters = [
        vote.participant.name
        for vote in unavailable_votes
    ]

    # 코드 → 한글 변환용
    weekday_map = dict(
        AvailabilityVote.Weekday.choices
    )

    meal_map = dict(
        AvailabilityVote.MealType.choices
    )

    for vote in vote_results:

        vote["weekday_display"] = weekday_map.get(
            vote["weekday"],
            vote["weekday"],
        )

        vote["meal_display"] = meal_map.get(
            vote["meal_type"],
            vote["meal_type"],
        )

        # 해당 요일/식사에 투표한 사람
        voters = (
            meeting.availability_votes
            .filter(
                weekday=vote["weekday"],
                meal_type=vote["meal_type"],
            )
            .select_related("participant")
        )

        vote["voters"] = [
            v.participant.name
            for v in voters
        ]

    top_vote = vote_results[0] if vote_results else None

    # -----------------------------
    # 모임 확정
    # -----------------------------

    if request.method == "POST":

        form = MeetingConfirmForm(
            request.POST,
            instance=meeting,
        )

        if form.is_valid():

            meeting = form.save(commit=False)

            meeting.status = Meeting.Status.CONFIRMED

            meeting.save()

            return redirect(
                "manager:meeting_detail",
                meeting.id,
            )

    else:

        form = MeetingConfirmForm(
            instance=meeting,
        )

    return render(
        request,
        "manager/meeting_detail.html",
        {
            "meeting": meeting,
            "form": form,
            "vote_results": vote_results,
            "top_vote": top_vote,
            "unavailable_count": unavailable_count,
            "unavailable_voters": unavailable_voters,
        },
    )


def attendance_result(request, meeting_id):

    meeting = get_object_or_404(
        Meeting,
        pk=meeting_id,
    )

    attendances = (
        Attendance.objects
        .filter(meeting=meeting)
        .select_related("participant")
        .order_by("participant__name")
    )

    attend_count = attendances.filter(
        status=Attendance.Status.ATTEND
    ).count()

    absent_count = attendances.filter(
        status=Attendance.Status.ABSENT
    ).count()

    return render(
        request,
        "manager/attendance_result.html",
        {
            "meeting": meeting,
            "attendances": attendances,
            "attend_count": attend_count,
            "absent_count": absent_count,
        },
    )
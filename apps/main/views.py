from django.shortcuts import redirect, render

from apps.survey.models import Participant

from apps.notice.models import Notice

from apps.meeting.models import Meeting

def home(request):
    participant_id = request.session.get("participant_id")

    participant = None

    if participant_id:
        participant = Participant.objects.filter(
            id=participant_id
        ).first()

    return render(
        request,
        "main/home.html",
        {
            "participant": participant,
        },
    )


def dashboard(request):
    participant_id = request.session.get("participant_id")

    confirmed_meeting = (
        Meeting.objects.filter(
            status=Meeting.Status.CONFIRMED,
        )
        .order_by("-meeting_date")
        .first()
    )

    voting_meeting = (
        Meeting.objects.filter(
            status=Meeting.Status.VOTING,
        )
        .order_by("-created_at")
        .first()
    )

    meeting = confirmed_meeting or voting_meeting

    if not participant_id:
        return redirect("survey:enter")

    try:
        participant = Participant.objects.get(
            id=participant_id,
            is_active=True,
        )
    except Participant.DoesNotExist:
        request.session.flush()
        return redirect("survey:enter")

    notices = Notice.objects.filter(
        is_published=True,
    ).order_by("-created_at")[:5]

    return render(
        request,
        "main/dashboard.html",
        {
            "participant": participant,
            "notices": notices,
            "meeting": meeting,
        },
    )
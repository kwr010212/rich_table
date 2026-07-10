from django.shortcuts import redirect, render

from apps.survey.models import Participant


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

    return render(
        request,
        "main/dashboard.html",
        {
            "participant": participant,
        },
    )
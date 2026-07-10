from django.shortcuts import redirect, render

from .forms import EnterForm, ParticipantForm
from .models import Participant


def enter(request):
    form = EnterForm(request.POST or None)
    participant = None

    if request.method == "POST" and form.is_valid():

        try:
            participant = Participant.objects.get(
                name=form.cleaned_data["name"],
                campus=form.cleaned_data["campus"],
                is_active=True,
            )

            request.session["participant_id"] = participant.id

            return redirect("main:dashboard")

        except Participant.DoesNotExist:
            form.add_error(
                None,
                "등록된 참여자를 찾을 수 없습니다. 이름과 캠퍼스를 다시 확인해주세요."
            )

    return render(
        request,
        "survey/enter.html",   # ← 이 부분도 중요!
        {
            "form": form,
        },
    )

def register(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)

        if form.is_valid():
            participant = form.save()

            request.session["participant_name"] = participant.name
            request.session["participant_campus"] = participant.campus

            return redirect("survey:register_complete")

    else:
        form = ParticipantForm()

    return render(
        request,
        "survey/register.html",
        {
            "form": form,
        },
    )


def register_complete(request):
    return render(request, "survey/register_complete.html")
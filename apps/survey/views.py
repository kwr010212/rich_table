from django.shortcuts import redirect, render

from .forms import ParticipantForm


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
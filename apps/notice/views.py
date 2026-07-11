from django.shortcuts import get_object_or_404, render

from .models import Notice


def detail(request, notice_id):
    notice = get_object_or_404(
        Notice,
        pk=notice_id,
        is_published=True,
    )

    return render(
        request,
        "notice/detail.html",
        {
            "notice": notice,
        },
    )
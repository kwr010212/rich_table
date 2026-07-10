from django.contrib import admin

from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "vote_start",
        "vote_end",
        "meeting_date",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "title",
    )
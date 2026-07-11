from django.contrib import admin

from .models import (
    Meeting,
    MeetingCandidate,
    AvailabilityVote,
    Attendance,
)




class MeetingCandidateInline(admin.TabularInline):
    model = MeetingCandidate
    extra = 1

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    inlines = [MeetingCandidateInline]
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

    ordering = (
        "-created_at",
    )

    inlines = [
        MeetingCandidateInline,
    ]

@admin.register(AvailabilityVote)
class AvailabilityVoteAdmin(admin.ModelAdmin):
    list_display = (
        "participant",
        "meeting",
        "weekday",
        "meal_type",
    )

    list_filter = (
        "meeting",
        "weekday",
        "meal_type",
    )

    search_fields = (
        "participant__name",
    )

@admin.register(MeetingCandidate)
class MeetingCandidateAdmin(admin.ModelAdmin):
    list_display = (
        "meeting",
        "weekday",
        "meal_type",
    )

    list_filter = (
        "meeting",
        "weekday",
        "meal_type",
    )

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "meeting",
        "participant",
        "status",
        "created_at",
    )

    list_filter = (
        "meeting",
        "status",
    )

    search_fields = (
        "participant__name",
    )

    ordering = (
        "meeting",
        "participant__name",
    )
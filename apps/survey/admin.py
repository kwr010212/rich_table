from django.contrib import admin

from .models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "campus",
        "student_id",
        "is_active",
        "created_at",
    )

    list_filter = (
        "campus",
        "is_active",
    )

    search_fields = (
        "name",
        "student_id",
    )

    ordering = (
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "기본 정보",
            {
                "fields": (
                    "name",
                    "campus",
                    "student_id",
                )
            },
        ),
        (
            "음식",
            {
                "fields": (
                    "favorite_food",
                    "disliked_food",
                )
            },
        ),
        (
            "관리",
            {
                "fields": (
                    "is_active",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
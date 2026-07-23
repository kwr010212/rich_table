from django import forms

from .models import (
    MeetingCandidate,
    Attendance,
)
from django.db.models import Case, When, IntegerField

class AvailabilityVoteForm(forms.Form):

    candidates = forms.ModelMultipleChoiceField(
        queryset=MeetingCandidate.objects.none(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input",
            }
        ),
        label="가능한 시간을 선택해주세요.",
    )

    def __init__(self, *args, meeting=None, **kwargs):
        super().__init__(*args, **kwargs)

        if meeting:
            self.fields["candidates"].queryset = (
                meeting.candidates
                .annotate(
                    weekday_order=Case(
                        When(weekday="MON", then=0),
                        When(weekday="TUE", then=1),
                        When(weekday="WED", then=2),
                        When(weekday="THU", then=3),
                        When(weekday="FRI", then=4),
                        When(weekday="SAT", then=5),
                        output_field=IntegerField(),
                    ),
                    meal_order=Case(
                        When(meal_type="LUNCH", then=0),
                        When(meal_type="DINNER", then=1),
                        output_field=IntegerField(),
                    ),
                )
                .order_by("weekday_order", "meal_order")
            )

class AttendanceForm(forms.Form):

    status = forms.ChoiceField(
        label="참석 여부",
        choices=Attendance.Status.choices,
        widget=forms.RadioSelect(
            attrs={
                "class": "form-check-input",
            }
        ),
    )   
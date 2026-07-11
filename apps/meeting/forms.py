from django import forms

from .models import (
    MeetingCandidate,
    Attendance,
)


class AvailabilityVoteForm(forms.Form):

    candidates = forms.ModelMultipleChoiceField(
        queryset=MeetingCandidate.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="가능한 시간을 선택해주세요.",
    )

    def __init__(self, *args, meeting=None, **kwargs):
        super().__init__(*args, **kwargs)

        if meeting:
            self.fields["candidates"].queryset = (
                meeting.candidates.all()
            )

class AttendanceForm(forms.Form):

    status = forms.ChoiceField(
        label="참석 여부",
        choices=Attendance.Status.choices,
        widget=forms.RadioSelect,
    )   
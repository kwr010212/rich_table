from django import forms

from apps.meeting.models import Meeting


class MeetingForm(forms.ModelForm):

    class Meta:
        model = Meeting

        fields = [
            "title",
            "description",
            "vote_start",
            "vote_end",
        ]

        widgets = {
            "vote_start": forms.DateInput(
                attrs={"type": "date"}
            ),
            "vote_end": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 3}
            ),
        }

        labels = {
            "title": "모임명",
            "description": "설명",
            "vote_start": "투표 시작일",
            "vote_end": "투표 종료일",
        }

class MeetingConfirmForm(forms.ModelForm):

    class Meta:
        model = Meeting

        fields = [
            "meeting_date",
            "meal_type",
            "meeting_time",
            "location",
        ]

        widgets = {
            "meeting_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "meeting_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
        }

        labels = {
            "meeting_date": "모임 날짜",
            "meal_type": "식사",
            "meeting_time": "모임 시간",
            "location": "장소",
        }
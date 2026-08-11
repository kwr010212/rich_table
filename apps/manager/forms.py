from django import forms

from apps.meeting.models import Meeting


class MeetingForm(forms.ModelForm):

    available_slots = forms.MultipleChoiceField(
        label="가능한 시간",
        choices=[
            ("MON_LUNCH", "월요일 점심"),
            ("MON_DINNER", "월요일 저녁"),

            ("TUE_LUNCH", "화요일 점심"),
            ("TUE_DINNER", "화요일 저녁"),

            ("WED_LUNCH", "수요일 점심"),
            ("WED_DINNER", "수요일 저녁"),

            ("THU_LUNCH", "목요일 점심"),
            ("THU_DINNER", "목요일 저녁"),

            ("FRI_LUNCH", "금요일 점심"),
            ("FRI_DINNER", "금요일 저녁"),

            ("SAT_LUNCH", "토요일 점심"),
            ("SAT_DINNER", "토요일 저녁"),
        ],
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-check-input",
            }
        ),
        required=True,
        error_messages={
            "required": "가능한 시간을 하나 이상 선택해주세요.",
        },
    )

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
                attrs={
                    "type": "date",
                }
            ),
            "vote_end": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                }
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
                attrs={
                    "type": "date",
                }
            ),
            "meeting_time": forms.TimeInput(
                attrs={
                    "type": "time",
                }
            ),
        }

        labels = {
            "meeting_date": "최종 날짜",
            "meal_type": "식사 시간",
            "meeting_time": "모임 시간",
            "location": "장소",
        }
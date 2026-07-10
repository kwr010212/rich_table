from django import forms

from .models import Participant


class ParticipantForm(forms.ModelForm):

    class Meta:
        model = Participant

        fields = [
            "name",
            "campus",
            "student_id",
            "favorite_food",
            "disliked_food",
        ]

        labels = {
            "name": "이름",
            "campus": "캠퍼스",
            "student_id": "학번",
            "favorite_food": "먹고 싶은 음식",
            "disliked_food": "못 먹는 음식",
        }

        help_texts = {
            "favorite_food": "쉼표(,)로 여러 개 입력할 수 있습니다.",
            "disliked_food": "쉼표(,)로 여러 개 입력할 수 있습니다.",
        }

        widgets = {
            "campus": forms.RadioSelect(),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "이름을 입력해주세요",
                }
            ),

            "student_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "학번을 입력해주세요",
                }
            ),

            "favorite_food": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "예) 삼겹살, 초밥, 파스타",
                }
            ),

            "disliked_food": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "예) 오이, 갑각류",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get("name")
        campus = cleaned_data.get("campus")

        if (
            name
            and campus
            and Participant.objects.filter(
                name=name,
                campus=campus,
            ).exists()
        ):
            raise forms.ValidationError(
                "이미 등록된 참여자입니다. 참여하기를 이용해주세요."
            )

        return cleaned_data


class EnterForm(forms.Form):

    name = forms.CharField(
        label="이름",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "이름을 입력해주세요",
            }
        ),
    )

    campus = forms.ChoiceField(
        label="캠퍼스",
        choices=Participant._meta.get_field("campus").choices,
        widget=forms.RadioSelect(),
    )
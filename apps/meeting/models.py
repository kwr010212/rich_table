from django.db import models
from django.db.models import Case, When, IntegerField


class Meeting(models.Model):

    class Status(models.TextChoices):
        VOTING = "VOTING", "요일 투표중"
        CONFIRMED = "CONFIRMED", "모임 확정"
        FINISHED = "FINISHED", "종료"

    title = models.CharField(
        "모임명",
        max_length=100,
    )

    description = models.TextField(
        "설명",
        blank=True,
    )

    vote_start = models.DateField(
        "투표 시작일",
    )

    vote_end = models.DateField(
        "투표 종료일",
    )

    status = models.CharField(
        "상태",
        max_length=20,
        choices=Status.choices,
        default=Status.VOTING,
    )

    # ▼ 관리자가 투표 종료 후 입력
    meeting_date = models.DateField(
        "최종 날짜",
        null=True,
        blank=True,
    )

    class MealType(models.TextChoices):
        LUNCH = "LUNCH", "점심"
        DINNER = "DINNER", "저녁"

    meal_type = models.CharField(
        "식사 시간",
        max_length=10,
        choices=MealType.choices,
        null=True,
        blank=True,
    )

    meeting_time = models.TimeField(
        "모임 시간",
        null=True,
        blank=True,
    )

    location = models.CharField(
        "장소",
        max_length=100,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "모임"
        verbose_name_plural = "모임"

    def __str__(self):
        return self.title
    

class AvailabilityVote(models.Model):

    class Weekday(models.TextChoices):
        MON = "MON", "월요일"
        TUE = "TUE", "화요일"
        WED = "WED", "수요일"
        THU = "THU", "목요일"
        FRI = "FRI", "금요일"
        SAT = "SAT", "토요일"

    class MealType(models.TextChoices):
        LUNCH = "LUNCH", "점심"
        DINNER = "DINNER", "저녁"

    meeting = models.ForeignKey(
        "meeting.Meeting",
        on_delete=models.CASCADE,
        related_name="availability_votes",
    )

    participant = models.ForeignKey(
        "survey.Participant",
        on_delete=models.CASCADE,
        related_name="availability_votes",
    )

    weekday = models.CharField(
        max_length=3,
        choices=Weekday.choices,
    )

    meal_type = models.CharField(
        max_length=10,
        choices=MealType.choices,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "meeting",
            "participant",
            "weekday",
            "meal_type",
        )

    def __str__(self):
        return f"{self.participant} - {self.get_weekday_display()} {self.get_meal_type_display()}"
    
class Attendance(models.Model):

    class Status(models.TextChoices):
        ATTEND = "ATTEND", "참석"
        ABSENT = "ABSENT", "불참"

    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    participant = models.ForeignKey(
        "survey.Participant",
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "meeting",
            "participant",
        )

    def __str__(self):
        return f"{self.participant} - {self.get_status_display()}"

class MeetingCandidate(models.Model):

    class Weekday(models.TextChoices):
        MON = "MON", "월요일"
        TUE = "TUE", "화요일"
        WED = "WED", "수요일"
        THU = "THU", "목요일"
        FRI = "FRI", "금요일"
        SAT = "SAT", "토요일"

    class MealType(models.TextChoices):
        LUNCH = "LUNCH", "점심"
        DINNER = "DINNER", "저녁"

    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name="candidates",
    )

    weekday = models.CharField(
        max_length=3,
        choices=Weekday.choices,
    )

    meal_type = models.CharField(
        max_length=10,
        choices=MealType.choices,
    )

    class Meta:
        unique_together = (
            "meeting",
            "weekday",
            "meal_type",
        )

    def __str__(self):
        return f"{self.get_weekday_display()} {self.get_meal_type_display()}"

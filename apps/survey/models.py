from django.db import models


class Campus(models.TextChoices):
    JEONJUUNIV = "JEONJUUNIV", "전주대"
    VISIONUNIV = "VISIONUNIV", "비전대"
    JESUSUNIV = "JESUSUNIV", "예수대"
    KIJEONUNIV = "KIJEONUNIV", "기전대"
    AFUNIV = "AFUNIV", "한국농수산대"


class Participant(models.Model):
    """프로그램 참여자"""

    name = models.CharField(
        max_length=30,
        verbose_name="이름",
    )

    campus = models.CharField(
        max_length=20,
        choices=Campus.choices,
        verbose_name="캠퍼스",
    )

    student_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="학번",
    )

    favorite_food = models.TextField(
        blank=True,
        verbose_name="먹고 싶은 음식",
        help_text="쉼표(,)로 구분해서 입력해주세요.",
    )

    disliked_food = models.TextField(
        blank=True,
        verbose_name="못 먹는 음식",
        help_text="쉼표(,)로 구분해서 입력해주세요.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="등록일",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="수정일",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="활성 여부",
    )

    class Meta:
        verbose_name = "참여자"
        verbose_name_plural = "참여자"

        constraints = [
            models.UniqueConstraint(
                fields=["name", "campus"],
                name="unique_participant",
            )
        ]

        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_campus_display()})"
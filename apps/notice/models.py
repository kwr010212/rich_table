from django.db import models


class Notice(models.Model):

    title = models.CharField(
        "제목",
        max_length=100,
    )

    content = models.TextField(
        "내용",
    )

    is_published = models.BooleanField(
        "게시 여부",
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "공지사항"
        verbose_name_plural = "공지사항"

    def __str__(self):
        return self.title
from django.db import models
from apps.programs.models import Program

# 교육 신청 테이블
class Application(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "RECEIVED", "접수"
        REVIEWING = "REVIEWING", "확인중"
        COMPLETED = "COMPLETED", "완료"

    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name="applications",
        verbose_name="신청 교육 과정",
    )

    applicant_name = models.CharField(max_length=50, verbose_name="신청자 이름")
    email = models.EmailField(verbose_name="이메일")
    address = models.CharField(max_length=255, verbose_name="주소")
    available_date = models.DateField(verbose_name="연락 가능 날짜")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RECEIVED,
        verbose_name="신청 상태",
    )
    is_reminded = models.BooleanField(default=False, verbose_name="안내 메일 발송 여부")
    admin_memo = models.TextField(blank=True, verbose_name="관리자 메모")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="신청일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        db_table = "applications"
        ordering = ["-created_at"]
        verbose_name = "교육 신청"
        indexes = [
            models.Index(fields=["available_date", "is_reminded"]),
            models.Index(fields=["status"]),
        ]
        verbose_name_plural = "교육 신청 목록"

    def __str__(self) -> str:
        return f"[{self.get_status_display()}] {self.applicant_name} - {self.program.title}"
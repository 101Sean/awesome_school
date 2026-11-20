from django.db import models

# 교육 과정 테이블
class Program(models.Model):
    title = models.CharField(max_length=150, verbose_name="교육명")
    subtitle = models.CharField(max_length=255, verbose_name="한 줄 소개")
    description = models.TextField(blank=True, verbose_name="상세 설명")
    curriculum = models.JSONField(default=list, verbose_name="커리큘럼")
    thumbnail_url = models.URLField(blank=True, verbose_name="대표 이미지 URL")
    is_active = models.BooleanField(default=True, verbose_name="모집 활성화 여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        db_table = "programs"
        ordering = ["-created_at"]
        verbose_name = "교육 과정"
        verbose_name_plural = "교육 과정 목록"

    def __str__(self) -> str:
        return self.title
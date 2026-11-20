from django.utils import timezone
from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    program_title = serializers.CharField(source="program.title", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id",
            "program",
            "program_title",
            "applicant_name",
            "email",
            "address",
            "available_date",
            "status",
            "status_display",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]

    def validate_available_date(self, value):
        if value < timezone.localdate():
            raise serializers.ValidationError("연락 가능 날짜는 오늘 이후 날짜로 선택해 주세요.")
        return value

    def validate(self, attrs):
        exists = Application.objects.filter(
            program=attrs.get("program"),
            email=attrs.get("email"),
            status__in=[Application.Status.RECEIVED, Application.Status.REVIEWING],
        ).exists()
        if exists:
            raise serializers.ValidationError({"email": "해당 교육 과정에 이미 진행 중인 신청 내역이 존재합니다."})
        return attrs


class ApplicationAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id",
            "applicant_name",
            "email",
            "address",
            "available_date",
            "status",
            "admin_memo",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]
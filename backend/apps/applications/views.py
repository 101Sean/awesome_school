from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import generics, permissions
from .models import Application
from .serializers import ApplicationSerializer, ApplicationAdminUpdateSerializer

from io import StringIO
from django.core.management import call_command
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import export_applications_to_google_sheet


class ManageDashboardView(LoginRequiredMixin, TemplateView):
    """관리자 전용 신청 내역 대시보드 (GET /manage/)"""
    template_name = "manage.html"
    login_url = "/admin/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_count"] = Application.objects.count()
        context["received_count"] = Application.objects.filter(status=Application.Status.RECEIVED).count()
        context["reviewing_count"] = Application.objects.filter(status=Application.Status.REVIEWING).count()
        context["completed_count"] = Application.objects.filter(status=Application.Status.COMPLETED).count()
        return context


class ApplicationListCreateView(generics.ListCreateAPIView):
    """신청 목록 조회(GET: 관리자 전용) 및 교육 신청 접수(POST: 누구나 가능)"""
    serializer_class = ApplicationSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        queryset = Application.objects.select_related("program").all()
        status_param = self.request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """개별 신청 조회(GET), 수정(PATCH/PUT), 삭제(DELETE) - 관리자 전용"""
    queryset = Application.objects.select_related("program").all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ApplicationAdminUpdateSerializer
        return ApplicationSerializer


class TriggerReminderEmailView(APIView):
    """관리자 대시보드에서 안내 메일 발송 배치를 수동 실행하는 API (POST)"""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        target_date = request.data.get("date")
        out = StringIO()
        if target_date:
            call_command("send_reminders", date=target_date, stdout=out)
        else:
            call_command("send_reminders", stdout=out)

        output_text = out.getvalue().strip()
        return Response(
            {"message": output_text or "안내 메일 발송 배치를 실행했습니다."},
            status=status.HTTP_200_OK,
        )


class ExportGoogleSheetView(APIView):
    """관리자 대시보드에서 Google Spreadsheet로 신청 내역을 내보내는 API (POST)"""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        try:
            result = export_applications_to_google_sheet()
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": f"스프레드시트 동기화 중 오류가 발생했습니다: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
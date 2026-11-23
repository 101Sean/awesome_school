from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import generics, permissions
from .models import Application
from .serializers import ApplicationSerializer, ApplicationAdminUpdateSerializer


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
from django.views.generic import TemplateView
from rest_framework import generics
from .models import Program
from .serializers import ProgramSerializer


class LandingPageView(TemplateView):
    """교육 소개 및 신청 메인 페이지 (GET /)"""
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["programs"] = Program.objects.filter(is_active=True).order_by("id")
        return context


class ProgramListView(generics.ListAPIView):
    """활성화된 교육 과정 목록 조회 (GET /api/programs/)"""
    queryset = Program.objects.filter(is_active=True).order_by("id")
    serializer_class = ProgramSerializer


class ProgramDetailView(generics.RetrieveAPIView):
    """특정 교육 과정 상세 조회 (GET /api/programs/<id>/)"""
    queryset = Program.objects.filter(is_active=True)
    serializer_class = ProgramSerializer
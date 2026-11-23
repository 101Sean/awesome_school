from django.contrib import admin
from django.urls import path, include
from apps.programs.views import LandingPageView
from apps.applications.views import ManageDashboardView

urlpatterns = [
    path("", LandingPageView.as_view(), name="home"),
    path("manage/", ManageDashboardView.as_view(), name="manage-dashboard"),
    path("admin/", admin.site.urls),
    path("api/programs/", include("apps.programs.urls")),
    path("api/applications/", include("apps.applications.urls")),
]
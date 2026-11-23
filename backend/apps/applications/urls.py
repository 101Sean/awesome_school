from django.urls import path
from .views import (
    ApplicationListCreateView,
    ApplicationDetailView,
    TriggerReminderEmailView,
    ExportGoogleSheetView,
)

urlpatterns = [
    path("", ApplicationListCreateView.as_view(), name="application-list-create"),
    path("<int:pk>/", ApplicationDetailView.as_view(), name="application-detail"),
    path("actions/send-reminders/", TriggerReminderEmailView.as_view(), name="trigger-reminders"),
    path("actions/export-sheets/", ExportGoogleSheetView.as_view(), name="export-sheets"),
]
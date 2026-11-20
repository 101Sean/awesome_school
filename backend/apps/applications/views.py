from rest_framework import generics
from .models import Application
from .serializers import ApplicationSerializer, ApplicationAdminUpdateSerializer


class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        queryset = Application.objects.select_related("program").all()
        status_param = self.request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.select_related("program").all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ApplicationAdminUpdateSerializer
        return ApplicationSerializer

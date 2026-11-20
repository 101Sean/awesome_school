from rest_framework import serializers
from .models import Program


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            "id",
            "title",
            "subtitle",
            "description",
            "curriculum",
            "thumbnail_url",
            "is_active",
        ]
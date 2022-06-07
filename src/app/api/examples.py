import logging
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from app.models import Example

logger = logging.getLogger(__package__)


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = "__all__"


class ExampleViewSet(ModelViewSet):
    serializer_class = ExampleSerializer

    def get_queryset(self):
        queryset = Example.objects.filter()
        project = self.request.query_params.get("project")
        if project:
            queryset = queryset.filter(project=project)
        return queryset

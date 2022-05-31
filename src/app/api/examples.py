import logging
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from app.models import Example, ExampleStatus

logger = logging.getLogger(__package__)


class ExampleStatusSerializer(serializers.Field):
    def to_representation(self, value):
        try:
            return ExampleStatus(value).name
        except ValueError:
            logger.error("Invalid ExampleStatus value {}".format(value))
            return ExampleStatus.pending.name

    def to_internal_value(self, name):
        try:
            return ExampleStatus[name].value
        except KeyError:
            logger.error("Invalid ExampleStatus name {}".format(name))
            return ExampleStatus.pending.value


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = "__all__"

    status = ExampleStatusSerializer()


class ExampleViewSet(ModelViewSet):
    serializer_class = ExampleSerializer

    def get_queryset(self):
        queryset = Example.objects.filter(is_deleted=False)
        project = self.request.query_params.get("project")
        if project:
            queryset = queryset.filter(project=project)
        return queryset

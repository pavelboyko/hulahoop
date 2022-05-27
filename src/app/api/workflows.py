from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from app.models import Workflow


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = (
            "id",
            "name",
            "properties",
            "created_by",
            "is_deleted",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"created_by": {"default": serializers.CurrentUserDefault()}}


class WorkflowViewSet(ModelViewSet):
    queryset = Workflow.objects.filter(is_deleted=False)
    serializer_class = WorkflowSerializer

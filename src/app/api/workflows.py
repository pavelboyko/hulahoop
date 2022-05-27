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
            "created_at",
            "updated_at",
            "is_deleted",
        )
        extra_kwargs = {"created_by": {"default": serializers.CurrentUserDefault()}}


class WorkflowViewSet(ModelViewSet):
    serializer_class = WorkflowSerializer
    queryset = Workflow.objects.filter(is_deleted=False)

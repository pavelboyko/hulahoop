from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from app.models import Example


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = (
            "id",
            "workflow",
            "properties",
            "created_at",
            "updated_at",
            "is_deleted",
        )


class ExampleViewSet(ModelViewSet):
    serializer_class = ExampleSerializer

    def get_queryset(self):
        queryset = Example.objects.filter(is_deleted=False)
        workflow = self.request.query_params.get("workflow")
        if workflow:
            queryset = queryset.filter(workflow=workflow)
        return queryset

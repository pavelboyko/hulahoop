import logging
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from app.models import Example, Project, ExampleTag


logger = logging.getLogger(__package__)


class ExampleSerializer(serializers.ModelSerializer):
    tags = serializers.JSONField(allow_null=True, required=False)

    class Meta:
        model = Example
        fields = [
            "media_url",
            "fingerprint",
            "predictions",
            "properties",
            "tags",
        ]

    def create(self, validated_data) -> Example:
        tags = validated_data.pop("tags") if "tags" in validated_data else None
        example = Example.objects.create(**validated_data)
        if tags is not None and type(tags) is dict:
            for key, value in tags.items():
                ExampleTag.objects.create(
                    example=example, key=str(key)[:32], value=str(value)[:255]
                )
        return example


@api_view(["POST"])
def capture(request, project_id: int) -> Response:
    """The public POST-only /api/capture/<project_id>/ endpoint to receive examples"""
    project = get_object_or_404(Project, pk=project_id)
    serializer = ExampleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)  # return 400 on invalid request data
    serializer.save(project=project)
    return Response(data={"status": 1}, status=status.HTTP_200_OK)

from rest_framework import serializers


class BadRequestSerializer(serializers.Serializer):
    """Serializer for BAD_REQUEST response."""

    field_name = serializers.ListField(child=serializers.CharField())


class ErrorSerializer(serializers.Serializer):
    """Serializer for ERROR response."""

    detail = serializers.CharField()
    code = serializers.CharField()

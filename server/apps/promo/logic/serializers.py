from rest_framework import serializers

from server.apps.promo.models import Promo


class PromoSerializer(serializers.ModelSerializer):
    """Serializer definition for Promo model."""

    class Meta:
        model = Promo
        fields = (
            "id",
            "code",
            "discount",
            "start",
            "end",
            "updated_at",
            "created_at",
        )
        read_only_fields = (
            "id",
            "updated_at",
            "created_at",
        )

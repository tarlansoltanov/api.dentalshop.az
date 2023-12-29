from rest_framework import serializers

from server.apps.account.models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "birth_date",
            "phone",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "birth_date": {"required": False},
        }
        read_only_fields = ("phone",)

    def update(self, instance: User, validated_data: dict):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)

        instance.save()

        return instance

from rest_framework import serializers

from server.apps.auth.logic.utils import get_token_pair, send_otp_code
from server.apps.user.models import User


class TokenPairSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class AccessTokenSerializer(serializers.Serializer):
    access = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "birth_date", "phone", "password", "password_confirm")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate_phone(self, value):
        """Check if the phone number is according to the format."""

        if not value.isdigit() or len(value) != 9:
            raise serializers.ValidationError("Invalid phone number format. Format: 501234567")

        return value

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError({"password_confirm": "Passwords mismatch."})

        attrs.pop("password_confirm")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SendOTPCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("User with this phone number does not exist.")

        return value

    def create(self, validated_data):
        user = User.objects.get(phone=validated_data["phone"])

        send_otp_code(user)

        return user


class VerifyOTPCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp_code = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get("phone")
        otp_code = attrs.get("otp_code")

        user = User.objects.get(phone=phone)

        if not user.verify_otp_code(otp_code):
            raise serializers.ValidationError("Invalid OTP code.")

        return attrs

    def create(self, validated_data):
        user = User.objects.get(phone=validated_data["phone"])

        return get_token_pair(user)

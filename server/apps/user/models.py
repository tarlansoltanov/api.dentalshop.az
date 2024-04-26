import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from server.apps.user.logic.managers import CustomUserManager


class User(AbstractUser):
    """
    Custom user model. It is used to authenticate users by phone number.
    """

    username = None
    email = None

    phone = models.CharField(max_length=11, unique=True)

    birth_date = models.DateField(null=True, blank=True)

    code = models.CharField(max_length=255, null=True, blank=True)
    discount = models.PositiveIntegerField(default=0)
    device_token = models.CharField(max_length=255, null=True, blank=True)

    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_trans_id = models.CharField(max_length=255, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        """Meta definition for User model."""

        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self):
        """Unicode representation of User."""
        return f"{self.first_name} {self.last_name} - {self.phone}"

    def generate_otp_code(self):
        """Generate OTP code."""
        self.otp_code = random.randint(100000, 999999)
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp_code

    def verify_otp_code(self, otp_code):
        """Verify OTP code."""
        if self.otp_code != otp_code:
            return False

        if (timezone.now() - self.otp_created_at).seconds > 300:
            return False

        self.is_verified = True
        self.save()
        return True

from django.contrib.auth.models import AbstractUser
from django.db import models

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

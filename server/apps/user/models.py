import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from server.apps.user.logic.managers import CustomUserManager


class User(AbstractUser):
    """
    Custom user model. It is used to authenticate users by phone number.
    """

    username = None
    email = None

    phone = models.CharField(verbose_name=_("Phone"), max_length=11, unique=True)

    birth_date = models.DateField(verbose_name=_("Birth Date"), null=True, blank=True)

    code = models.CharField(verbose_name=_("Discount Code"), max_length=255, null=True, blank=True)
    discount = models.PositiveIntegerField(verbose_name=_("Discount"), default=0)
    device_token = models.CharField(verbose_name=_("Device Token"), max_length=255, null=True, blank=True)

    otp_code = models.CharField(verbose_name=_("OTP Code"), max_length=6, null=True, blank=True)
    otp_trans_id = models.CharField(verbose_name=_("OTP Transaction ID"), max_length=255, null=True, blank=True)
    otp_created_at = models.DateTimeField(verbose_name=_("OTP Created at"), null=True, blank=True)
    otp_used_at = models.DateTimeField(verbose_name=_("OTP Used at"), null=True, blank=True)

    is_verified = models.BooleanField(verbose_name=_("Is Verified"), default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

        ordering = ("-date_joined",)

    def __str__(self):
        """Unicode representation of User."""
        return f"{self.first_name} {self.last_name} - {self.phone}"

    def generate_otp_code(self):
        """Generate OTP code."""
        self.otp_code = random.randint(100000, 999999)
        self.otp_created_at = timezone.now()
        self.otp_used_at = None
        self.save()
        return self.otp_code

    def verify_otp_code(self, otp_code):
        """Verify OTP code."""
        if self.otp_code != otp_code:
            return False

        if (timezone.now() - self.otp_created_at).seconds > 300:
            return False

        if self.otp_used_at:
            return False

        self.otp_used_at = timezone.now()

        self.is_verified = True
        self.save()
        return True

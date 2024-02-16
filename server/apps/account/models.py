from django.contrib.auth.models import AbstractUser
from django.db import models

from server.apps.account.managers import CustomUserManager
from server.apps.core.models import CoreModel


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


class Favorite(CoreModel):
    """Model definition for Favorite."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="favorites")

    class Meta(CoreModel.Meta):
        """Meta definition for Favorite."""

        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

    def __str__(self):
        """Unicode representation of Favorite."""
        return f"{self.user} - {self.product}"


class Cart(CoreModel):
    """Model definition for Cart."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="cart")
    quantity = models.PositiveIntegerField(default=0)

    class Meta(CoreModel.Meta):
        """Meta definition for Cart."""

        verbose_name = "Cart"
        verbose_name_plural = "Cart"

    def __str__(self):
        """Unicode representation of Cart."""
        return f"{self.user} - {self.product}"

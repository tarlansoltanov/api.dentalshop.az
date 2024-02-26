from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from server.apps.user.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom Admin for User Model"""

    list_display = ("phone", "first_name", "last_name", "is_staff")
    ordering = ["-date_joined"]
    exclude = ("username", "email")
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("discount", {"fields": ("discount", "code")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birth_date",
                    "device_token",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2"),
            },
        ),
    )

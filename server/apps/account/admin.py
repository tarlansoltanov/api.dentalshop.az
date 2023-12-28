from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from server.apps.account.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("phone", "first_name", "last_name", "is_staff")
    ordering = ["-date_joined"]
    exclude = ("username", "email")
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "password",
                    "birth_date",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
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

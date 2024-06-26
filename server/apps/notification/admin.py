from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from server.apps.core.admin import ModelAdmin
from server.apps.notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    """Notification admin."""

    list_display = ("title", "body", "to")

    def to(self, obj):
        return _("All Users") if obj.user is None else obj.user

    to.short_description = _("To")

    search_fields = (
        "title",
        "body",
        "user__username",
    )

    autocomplete_fields = ("user",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "body",
                    "user",
                )
            },
        ),
    )

    def has_change_permission(self, request, obj=None):
        """Disable change permission."""
        return False

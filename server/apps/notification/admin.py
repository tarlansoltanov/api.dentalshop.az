from django.contrib import admin

from server.apps.notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "body",
        "user",
        "date",
        "updated_at",
        "created_at",
    )
    list_filter = (
        "date",
        "user",
    )
    search_fields = (
        "title",
        "body",
    )

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

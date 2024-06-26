from adminsortable2.admin import SortableAdminMixin as _SortableAdminMixin
from adminsortable2.admin import SortableStackedInline
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from server.apps.core.constants import API_PREFIX
from server.settings.components import config

PROJECT_NAME = config("PROJECT_NAME", default="Project", cast=str).capitalize()

# Text to put at the end of each page's <title>.
admin.site.site_title = "CodeShift Admin"

# Text to put in each page's <div id="site-name">.
admin.site.site_header = "CodeShift Admin"

# Text to put at the top of the admin index page.
admin.site.index_title = f'{PROJECT_NAME} {_("Site administration")}'

# URL for the "View site" link at the top of each admin page.
admin.site.site_url = f"/{API_PREFIX}"


class ModelAdmin(admin.ModelAdmin):
    """Model admin class template."""

    list_per_page = 20

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances.
        """
        self.request = request
        return super().get_queryset(request)

    def get_list_display(self, request):
        """
        Append the ``updated_at`` and ``created_at`` fields to the ``list_display`` attribute.
        """
        return super().get_list_display(request) + ("updated_at", "created_at", "operations")

    def get_list_filter(self, request):
        """
        Append the ``created_at`` fields to the ``list_filter`` attribute.
        """
        return super().get_list_filter(request) + ("created_at",)

    def get_readonly_fields(self, request, obj):
        """
        Append the ``updated_at`` and ``created_at`` fields to the ``readonly_fields`` attribute.
        """
        if obj:
            return super().get_readonly_fields(request, obj) + ("updated_at", "created_at")

        return super().get_readonly_fields(request, obj)

    def get_fieldsets(self, request, obj):
        """
        Append the ``updated_at`` and ``created_at`` fields to the ``fieldsets`` attribute.
        """
        fieldsets = list(super().get_fieldsets(request, obj))

        if obj:
            fieldsets.append(
                (
                    _("Date"),
                    {
                        "fields": (
                            "updated_at",
                            "created_at",
                        ),
                        "classes": ("collapse",),
                    },
                )
            )

        return fieldsets

    def operations(self, obj):
        """Display edit and delete buttons."""
        view_btn = f'<a href="/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/change/" class="button">{_("View")}</a>'  # noqa: E501
        edit_btn = f'<a href="/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/change/" class="button">{_("Change")}</a>'  # noqa: E501
        delete_btn = f'<a href="/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/delete/" class="button">{_("Delete")}</a>'  # noqa: E501

        btns = []

        if self.has_change_permission(self.request, obj):
            btns.append(edit_btn)
        else:
            btns.append(view_btn)

        if self.has_delete_permission(self.request, obj):
            btns.append(delete_btn)

        return mark_safe(f'<div class="submit-row" style="display: flex; gap: 10px;">{" ".join(btns)}</div>')

    operations.short_description = _("Operations")


class ImageAdminMixin:
    """Image model admin class template mixin."""

    image_field_name = "image"

    preview_attrs = {
        "width": "100px",
        "height": "100px",
    }

    def get_readonly_fields(self, request, obj):
        """
        Append the ``preview`` field to the ``readonly_fields`` attribute.
        """
        return super().get_readonly_fields(request, obj) + ("preview",)

    def preview(self, obj):
        """Display image preview."""
        image = getattr(obj, self.image_field_name)

        if not image:
            return _("No image")

        return mark_safe(
            f'<img src="{image.url}" style="{"; ".join([f"{k}: {v}" for k, v in self.preview_attrs.items()])}">'
        )

    preview.short_description = _("Preview")


class SortableAdminMixin(_SortableAdminMixin):
    """Sortable model admin class template."""

    def get_list_display(self, request):
        """
        Append the ``position`` field to the ``list_display`` attribute.
        """
        return super().get_list_display(request)


class ImageInlineAdmin(SortableStackedInline, ImageAdminMixin):
    """Image inline admin class template."""

    min_num = 1
    extra = 0

    verbose_name = _("Image")
    verbose_name_plural = _("Images")

    classes = ("collapse",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "image",
                    "preview",
                    "position",
                )
            },
        ),
    )

    readonly_fields = ("preview",)

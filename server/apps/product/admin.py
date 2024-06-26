from adminsortable2.admin import SortableAdminBase
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from server.apps.core.admin import ImageInlineAdmin, ModelAdmin, SortableAdminMixin
from server.apps.product.models import Product, ProductImage, ProductNote


class ProductImageInline(ImageInlineAdmin):
    """ProductImage Model inline admin configuration."""

    model = ProductImage


@admin.register(Product)
class ProductAdmin(SortableAdminBase, ModelAdmin):
    """Product Model admin configuration."""

    inlines = (ProductImageInline,)

    list_display = (
        "code",
        "name",
        "brand",
        "category",
        "price",
        "get_discount",
        "is_new",
    )

    list_filter = ("is_new",)

    def get_discount(self, obj):
        """Get discount for product."""
        return f"{obj.get_discount()}%"

    get_discount.short_description = _("Discount")

    search_fields = (
        "code",
        "name_az",
        "name_ru",
        "brand__name_az",
        "brand__name_ru",
        "category__name_az",
        "category__name_ru",
    )

    autocomplete_fields = ("brand", "category")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "code",
                    "name_az",
                    "name_ru",
                    "brand",
                    "category",
                    "price",
                    "quantity",
                    "is_new",
                    "is_distributer",
                )
            },
        ),
        (
            _("Discount"),
            {
                "fields": (
                    "is_promo",
                    "discount",
                    "discount_end_date",
                )
            },
        ),
        (
            _("Description"),
            {
                "fields": (
                    "main_note_az",
                    "main_note_ru",
                    "description_az",
                    "description_ru",
                )
            },
        ),
    )


@admin.register(ProductNote)
class ProductNoteAdmin(SortableAdminMixin, ModelAdmin):
    """Admin for ProductNote model."""

    list_display = ("text",)

    search_fields = (
        "text_az",
        "text_ru",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "text_az",
                    "text_ru",
                )
            },
        ),
    )

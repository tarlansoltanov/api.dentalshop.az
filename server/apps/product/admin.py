from django.contrib import admin

from server.apps.product.models import Product, ProductImage, ProductNote


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(ProductNote)
class ProductNoteAdmin(admin.ModelAdmin):
    """Admin for ProductNote model."""

    list_display = ["text_az", "text_ru"]
    search_fields = ["text_az", "text_ru"]

    fieldsets = ((None, {"fields": ("text_az", "text_ru")}),)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin for Product model."""

    inlines = (ProductImageInline,)

    list_display = (
        "name_az",
        "name_ru",
        "brand",
        "category",
        "price",
        "discount",
        "is_new",
        "in_stock",
        "is_distributer",
        "is_recommended",
    )

    list_filter = ("brand", "category", "is_new", "in_stock", "is_distributer")

    search_fields = (
        "name_az",
        "name_ru",
        "brand__name_az",
        "brand__name_ru",
        "category__name_az",
        "category__name_ru",
        "code",
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
                    "discount",
                    "is_new",
                    "in_stock",
                    "is_distributer",
                    "is_recommended",
                )
            },
        ),
        (
            "Description",
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

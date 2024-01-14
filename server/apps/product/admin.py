from django.contrib import admin

from server.apps.product.models import Product, ProductImage, ProductNote


class ProductNoteInline(admin.TabularInline):
    model = ProductNote.products.through
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(ProductNote)
class ProductNoteAdmin(admin.ModelAdmin):
    list_display = ["text"]
    search_fields = ["text"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductNoteInline, ProductImageInline]
    list_display = ["name", "brand", "category", "price", "discount", "in_stock", "is_distributer"]
    list_filter = ["brand", "category", "in_stock", "is_distributer"]
    search_fields = ["name", "brand__name", "category__name", "code"]
    autocomplete_fields = ["brand", "category"]
    readonly_fields = ["slug"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "slug",
                    "code",
                    "name",
                    "brand",
                    "category",
                    "price",
                    "discount",
                    "in_stock",
                    "is_distributer",
                )
            },
        ),
        ("Description", {"fields": ("main_note", "description")}),
    )

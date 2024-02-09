from modeltranslation.translator import register, TranslationOptions

from server.apps.product.models import Product, ProductNote


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    """Translation options for Product model."""

    fields = ("name", "main_note", "description")
    required_languages = ("az", "ru")


@register(ProductNote)
class ProductNoteTranslationOptions(TranslationOptions):
    """Translation options for ProductNote model."""

    fields = ("text",)
    required_languages = ("az", "ru")

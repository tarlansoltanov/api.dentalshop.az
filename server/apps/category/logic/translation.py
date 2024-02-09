from modeltranslation.translator import register, TranslationOptions

from server.apps.category.models import Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """Translation options for Category model."""

    fields = ("name",)
    required_languages = ("az", "ru")

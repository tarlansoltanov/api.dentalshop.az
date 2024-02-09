from modeltranslation.translator import register, TranslationOptions

from server.apps.brand.models import Brand


@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    """Translation options for Brand model."""

    fields = ("name",)
    required_languages = ("az", "ru")

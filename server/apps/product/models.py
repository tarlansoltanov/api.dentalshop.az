from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from server.apps.core.models import SlugModel, TimeStampedModel
from server.apps.product.logic.queryset import ProductQuerySet


class Product(TimeStampedModel, SlugModel):
    """Model definition for Product."""

    code = models.CharField(verbose_name=_("Code"), max_length=255, unique=True)
    name = models.CharField(verbose_name=_("Name"), max_length=255)

    brand = models.ForeignKey(
        to="brand.Brand", verbose_name=_("Brand"), related_name="products", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        to="category.Category", verbose_name=_("Category"), related_name="products", on_delete=models.CASCADE
    )

    price = models.DecimalField(verbose_name=_("Price"), max_digits=10, decimal_places=2, default=0)
    discount = models.PositiveIntegerField(verbose_name=_("Discount"), default=0)

    discount_end_date = models.DateField(verbose_name=_("Discount End Date"), null=True, blank=True)

    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"), default=0)

    is_promo = models.BooleanField(verbose_name=_("Is Promo"), default=True)

    is_new = models.BooleanField(verbose_name=_("Is New"), default=False)
    is_distributer = models.BooleanField(verbose_name=_("Is Distributer"), default=False)

    main_note = models.TextField(verbose_name=_("Main Note"), blank=True, null=True)
    description = models.TextField(verbose_name=_("Description"))

    objects = ProductQuerySet.as_manager()

    class Meta:
        """Meta definition for Product."""

        verbose_name = _("Product")
        verbose_name_plural = _("Products")

        ordering = ("-created_at",)

    def __str__(self):
        """Unicode representation of Product."""
        return self.name

    def generate_slug(self):
        return slugify(f"{self.name}-{self.code}")

    def get_discount(self):
        """Get discount for product."""
        if not self.discount:
            return 0

        if self.discount_end_date and self.discount_end_date < timezone.localtime(timezone.now()).date():
            return 0

        return self.discount

    def can_do_promo(self):
        """Check if product can do promo."""
        return self.is_promo and self.get_discount() == 0


class ProductImage(TimeStampedModel):
    """Model definition for ProductImage."""

    image = models.ImageField(verbose_name=_("Image"), upload_to="products")
    product = models.ForeignKey(
        to="product.Product", verbose_name=_("Product"), related_name="images", on_delete=models.CASCADE
    )

    class Meta(TimeStampedModel.Meta):
        """Meta definition for ProductImage."""

        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ("created_at",)

    def __str__(self):
        """Unicode representation of ProductImage."""
        return self.image.name


class ProductNote(TimeStampedModel):
    """Model definition for ProductNote."""

    text = models.TextField(verbose_name=_("Text"))

    class Meta(TimeStampedModel.Meta):
        """Meta definition for ProductNote."""

        verbose_name = _("Product Note")
        verbose_name_plural = _("Product Notes")

    def __str__(self):
        """Unicode representation of ProductNote."""
        return self.text

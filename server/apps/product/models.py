from django.db import models

from server.apps.core.models import CoreModel


class Product(CoreModel):
    """Model definition for Product."""

    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    brand = models.ForeignKey("brand.Brand", related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey("category.Category", related_name="products", on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.PositiveIntegerField(default=0)

    in_stock = models.BooleanField(default=True)
    is_distributer = models.BooleanField(default=False)

    notes = models.ManyToManyField("product.ProductNote", related_name="products")
    main_note = models.TextField()
    description = models.TextField()

    class Meta:
        """Meta definition for Product."""

        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        """Unicode representation of Product."""
        return self.name


class ProductImage(CoreModel):
    """Model definition for ProductImage."""

    image = models.ImageField(upload_to="products")
    product = models.ForeignKey("product.Product", related_name="images", on_delete=models.CASCADE)

    class Meta:
        """Meta definition for ProductImage."""

        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"

    def __str__(self):
        """Unicode representation of ProductImage."""
        return self.image.name


class ProductNote(CoreModel):
    """Model definition for ProductNote."""

    text = models.TextField()

    class Meta:
        """Meta definition for ProductNote."""

        verbose_name = "ProductNote"
        verbose_name_plural = "ProductNotes"

    def __str__(self):
        """Unicode representation of ProductNote."""
        return self.text

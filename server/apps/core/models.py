from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """

    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    class Meta:
        abstract = True


class SlugModel(TimeStampedModel):
    """
    An abstract base class model that provides a ``slug`` field.
    The timestamp fields for tracking the creation and update time are also included.
    """

    slug = models.SlugField(verbose_name=_("Slug"), max_length=255, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Save the model instance."""
        if not self.slug:
            self.slug = self.generate_slug()

        super().save(*args, **kwargs)

    def generate_slug(self):
        """
        Generate a unique slug for the model instance.
        """
        raise NotImplementedError("Method 'generate_slug' must be implemented in a subclass.")


class SortableModel(TimeStampedModel):
    """
    An abstract base class model that provides a ``position`` field.
    The timestamp fields for tracking the creation and update time are also included.
    """

    position = models.PositiveIntegerField(verbose_name=_("Position"), default=0, blank=False, null=False)

    class Meta:
        abstract = True


class ImageModel(models.Model):
    """
    An abstract base class model that provides an ``image`` field,
    a ``position`` field, timestamp fields and a method to display image preview.
    """

    image = models.ImageField(verbose_name=_("Image"))

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        """
        Initialize the model instance.
        """
        self._meta.get_field("image").upload_to = self.get_upload_path()
        super().__init__(*args, **kwargs)

    def get_upload_path(self):
        """
        Return the upload path for the image.
        """
        return "items/"


class ChildImageModel(ImageModel, SortableModel):
    """
    An abstract base class model that provides an ``image`` field,
    a ``position`` field, timestamp fields and a method to display image preview.
    """

    image = models.ImageField(verbose_name=_("Image"))

    class Meta:
        abstract = True

    def __str__(self):
        """
        Return the string representation of the model instance.
        """
        return self.image.name

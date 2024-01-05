import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from django.utils.text import slugify
from faker import Faker

from server.apps.brand.models import Brand
from server.apps.core.models import CoreModel

pytestmark = pytest.mark.django_db


def test_brand_model_inheritance():
    """Test that Brand model inherits from CoreModel."""

    assert issubclass(Brand, CoreModel)


def test_brand_model_fields():
    """Test that Brand model has all required fields."""

    assert hasattr(Brand, "photo")
    assert hasattr(Brand, "name")
    assert hasattr(Brand, "slug")


def test_brand_model_str(brand: Brand) -> None:
    """Test that Brand model str method returns correct value."""

    assert brand.name == str(brand)


def test_brand_model_save(brand: Brand) -> None:
    """Test that Brand model save method works correctly."""

    assert brand.slug == slugify(brand.name)


def test_brand_model_create(faker: Faker) -> None:
    """Test that Brand model create method works correctly."""

    brand_name = faker.company()
    brand = Brand.objects.create(name=brand_name)

    assert brand.name == brand_name
    assert brand.slug == slugify(brand_name)


def test_brand_model_update(faker: Faker, brand: Brand) -> None:
    """Test that Brand model update method works correctly."""

    brand_name = faker.company()
    brand.name = brand_name
    brand.save()

    assert brand.name == brand_name
    assert brand.slug == slugify(brand_name)


def test_brand_model_delete(brand: Brand):
    """Test that Brand model delete method works correctly."""

    brand.delete()

    assert Brand.objects.count() == 0


def test_brand_model_create_with_photo(faker: Faker) -> None:
    """Test that Brand model create method works correctly with photo."""

    brand_name = faker.company()
    brand = Brand.objects.create(name=brand_name, photo=SimpleUploadedFile("file.jpg", b"file_content"))

    assert brand.name == brand_name
    assert brand.slug == slugify(brand_name)
    assert brand.photo.name == "brands/file.jpg"


def test_brand_model_name_unique(faker: Faker):
    """Test that Brand model name field cannot be duplicated."""

    brand_name = faker.company()
    Brand.objects.create(name=brand_name)

    with pytest.raises(IntegrityError):
        Brand.objects.create(name=brand_name)


def test_brand_model_name_not_null():
    """Test that Brand model name field cannot be null."""

    with pytest.raises(IntegrityError):
        Brand.objects.create(name=None)

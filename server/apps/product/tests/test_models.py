import pytest
from django.db.utils import IntegrityError
from django.utils.text import slugify
from faker import Faker
from factory.django import DjangoModelFactory

from server.apps.core.models import CoreModel
from server.apps.product.models import ProductNote, Product

pytestmark = pytest.mark.django_db


# ProductNote model tests


def test_product_note_model_inheritance():
    """Test that ProductNote model inherits from CoreModel."""

    assert issubclass(ProductNote, CoreModel)


def test_product_note_model_fields():
    """Test that ProductNote model has all required fields."""

    assert hasattr(ProductNote, "text")


def test_product_note_model_str(product_note: ProductNote) -> None:
    """Test that ProductNote model str method returns correct value."""

    assert product_note.text == str(product_note)


def test_product_note_model_create(faker: Faker) -> None:
    """Test that ProductNote model create method works correctly."""

    product_note_text = faker.sentence()
    product_note = ProductNote.objects.create(text=product_note_text)

    assert product_note.text == product_note_text


def test_product_note_model_update(faker: Faker, product_note: ProductNote) -> None:
    """Test that ProductNote model update method works correctly."""

    product_note_text = faker.sentence()
    product_note.text = product_note_text
    product_note.save()

    assert product_note.text == product_note_text


def test_product_note_model_delete(product_note: ProductNote):
    """Test that ProductNote model delete method works correctly."""

    product_note.delete()

    assert ProductNote.objects.count() == 0


def test_product_note_model_text_not_null():
    """Test that ProductNote model text field cannot be null."""

    with pytest.raises(IntegrityError):
        ProductNote.objects.create(text=None)


# Product model tests


def test_product_model_inheritance():
    """Test that Product model inherits from CoreModel."""

    assert issubclass(Product, CoreModel)


def test_product_model_fields():
    """Test that Product model has all required fields."""

    assert hasattr(Product, "slug")
    assert hasattr(Product, "code")
    assert hasattr(Product, "name")
    assert hasattr(Product, "brand")
    assert hasattr(Product, "category")
    assert hasattr(Product, "price")
    assert hasattr(Product, "discount")
    assert hasattr(Product, "in_stock")
    assert hasattr(Product, "is_distributer")
    assert hasattr(Product, "notes")
    assert hasattr(Product, "main_note")
    assert hasattr(Product, "description")
    assert hasattr(Product, "images")


def test_product_model_str(product: Product) -> None:
    """Test that Product model str method returns correct value."""

    assert product.name == str(product)


def test_product_model_save(product: Product) -> None:
    """Test that Product model save method works correctly."""

    assert product.slug == slugify(product.name)


def test_product_model_create(product_factory: DjangoModelFactory) -> None:
    """Test that Product model create method works correctly."""

    product = product_factory.create()

    assert Product.objects.count() == 1
    assert product.slug == slugify(product.name)


def test_product_model_update(faker: Faker, product: Product) -> None:
    """Test that Product model update method works correctly."""

    product_name = faker.sentence()
    product.name = product_name
    product.save()

    assert product.name == product_name
    assert product.slug == slugify(product_name)


def test_product_model_delete(product: Product):
    """Test that Product model delete method works correctly."""

    product.delete()

    assert Product.objects.count() == 0

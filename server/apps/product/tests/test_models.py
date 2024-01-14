import pytest
from django.db.utils import IntegrityError
from faker import Faker

from server.apps.core.models import CoreModel
from server.apps.product.models import ProductNote

pytestmark = pytest.mark.django_db


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

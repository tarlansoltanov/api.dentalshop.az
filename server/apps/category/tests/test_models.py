import pytest
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from faker import Faker
from mptt.models import MPTTModel

from server.apps.category.models import Category
from server.apps.core.models import CoreModel

pytestmark = pytest.mark.django_db


def test_category_model_inheritance() -> None:
    """Test that Category model inherits from CoreModel."""

    assert issubclass(Category, CoreModel)
    assert issubclass(Category, MPTTModel)


def test_category_model_fields() -> None:
    """Test that Category model has all required fields."""

    assert hasattr(Category, "name")
    assert hasattr(Category, "slug")
    assert hasattr(Category, "parent")
    assert hasattr(Category, "children")


def test_category_model_str(category: Category) -> None:
    """Test that Category model str method returns correct value."""

    assert category.name == str(category)


def test_category_model_save(category: Category) -> None:
    """Test that Category model save method works correctly."""

    assert category.slug == slugify(category.name)


def test_category_model_create(faker: Faker) -> None:
    """Test that Category model create method works correctly."""

    category_name = faker.name()
    category = Category.objects.create(name=category_name)

    assert category.name == category_name
    assert category.slug == slugify(category_name)

    assert Category.objects.count() == 1


def test_category_model_update(faker: Faker, category: Category) -> None:
    """Test that Category model update method works correctly."""

    category_name = faker.name()
    category.name = category_name
    category.save()

    assert category.name == category_name
    assert category.slug == slugify(category_name)


def test_category_model_delete(category_factory: DjangoModelFactory) -> None:
    """Test that Category model delete method works correctly."""

    category = category_factory.create(level=0)

    assert Category.objects.count() == 1

    category.delete()

    assert Category.objects.count() == 0


def test_category_model_delete_sub_with_main(
    category_factory: DjangoModelFactory,
) -> None:
    """Test that Category model delete method works correctly with main category."""

    category = category_factory.create()
    category_factory.create(parent=category)

    assert Category.objects.count() == 2

    category.delete()

    assert Category.objects.count() == 0

import pytest
from django.urls import reverse
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from rest_framework import status
from rest_framework.test import APIClient

from server.apps.user.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def product_data(
    brand_factory: DjangoModelFactory, category_factory: DjangoModelFactory, product_note_factory: DjangoModelFactory
) -> dict:
    """Return product data."""
    return {
        "code": "PRODUCT34",
        "name": "Product",
        "brand": brand_factory.create().slug,
        "category": category_factory.create().slug,
        "price": 100,
        "discount": 0,
        "in_stock": True,
        "is_distributer": False,
        "main_note": "Main note",
        "description": "Description",
        "notes": [product_note_factory.create().id],
    }


def test_product_list_empty(api_client: APIClient) -> None:
    """Test product list endpoint with no products."""
    url = reverse("products:product-list")

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert response.data["count"] == 0


def test_product_list(api_client: APIClient, product_factory: DjangoModelFactory) -> None:
    """Test product list endpoint with products."""
    url = reverse("products:product-list")

    product_factory.create_batch(2)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert response.data["count"] == 2


def test_product_detail_invalid_slug(api_client: APIClient) -> None:
    """Test product detail endpoint with invalid slug."""
    url = reverse("products:product-detail", kwargs={"slug": "invalid"})

    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_product_detail_valid_slug(api_client: APIClient, product_factory: DjangoModelFactory) -> None:
    """Test product detail endpoint with valid slug."""
    product = product_factory.create()

    url = reverse("products:product-detail", kwargs={"slug": product.slug})

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert response.data["name"] == product.name
    assert response.data["slug"] == product.slug


def test_product_create_unauthenticated(api_client: APIClient, product_data: dict) -> None:
    """Test product create endpoint without authentication."""
    url = reverse("products:product-list")

    response = api_client.post(url, product_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_product_create_unauthorized(api_client: APIClient, user: User, product_data: dict) -> None:
    """Test product create endpoint without correct permissions."""
    url = reverse("products:product-list")

    api_client.force_authenticate(user=user)

    response = api_client.post(url, product_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_product_create_valid(api_client: APIClient, admin_user: User, temporary_image, product_data: dict) -> None:
    """Test product create endpoint with valid data and permissions."""
    url = reverse("products:product-list")

    api_client.force_authenticate(user=admin_user)

    response = api_client.post(url, product_data)
    assert response.status_code == status.HTTP_201_CREATED

    assert response.data["name"] == product_data["name"]
    assert response.data["slug"] == slugify(product_data["name"])


def test_product_update_unauthenticated(api_client: APIClient, product_factory: DjangoModelFactory) -> None:
    """Test product update endpoint without authentication."""
    product = product_factory.create()

    url = reverse("products:product-detail", kwargs={"slug": product.slug})

    data = {
        "name": "Product 12",
    }

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_product_update_unauthorized(api_client: APIClient, product_factory: DjangoModelFactory, user: User) -> None:
    """Test product update endpoint without correct permissions."""
    product = product_factory.create()

    url = reverse("products:product-detail", kwargs={"slug": product.slug})

    data = {
        "name": "Product 12",
    }

    api_client.force_authenticate(user=user)

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_product_update_invalid_slug(
    api_client: APIClient, product_factory: DjangoModelFactory, admin_user: User
) -> None:
    """Test product update endpoint with invalid slug but correct permissions."""
    url = reverse("products:product-detail", kwargs={"slug": "invalid"})

    data = {
        "name": "Product 12",
    }

    api_client.force_authenticate(user=admin_user)

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_product_update_valid(api_client: APIClient, product_factory: DjangoModelFactory, admin_user: User) -> None:
    """Test product update endpoint with valid data and permissions."""
    product = product_factory.create()

    url = reverse("products:product-detail", kwargs={"slug": product.slug})

    data = {
        "name": "Product 12",
    }

    api_client.force_authenticate(user=admin_user)

    response = api_client.put(url, data)
    print(response.data)
    assert response.status_code == status.HTTP_200_OK

    assert response.data["name"] == data["name"]
    assert response.data["slug"] == slugify(data["name"])


def test_product_delete_unauthenticated(api_client: APIClient, product_factory: DjangoModelFactory) -> None:
    """Test product delete endpoint without authentication."""
    product = product_factory.create()

    url = reverse("products:product-detail", kwargs={"slug": product.slug})

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_product_delete_unauthorized(api_client: APIClient, product_factory: DjangoModelFactory, user: User) -> None:
    """Test product delete endpoint without correct permissions."""
    product = product_factory.create()

    url = reverse("products:product-detail", kwargs={"slug": product.slug})

    api_client.force_authenticate(user=user)

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_product_delete_invalid_slug(api_client: APIClient, admin_user: User) -> None:
    """Test product delete endpoint with invalid slug but correct permissions."""
    url = reverse("products:product-detail", kwargs={"slug": "invalid"})

    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_product_delete_valid(api_client: APIClient, product_factory: DjangoModelFactory, admin_user: User) -> None:
    """Test product delete endpoint with valid data and permissions."""
    product = product_factory.create()

    url = reverse("products:product-detail", kwargs={"slug": product.slug})

    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert response.data is None

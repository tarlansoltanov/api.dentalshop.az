import pytest
from django.urls import reverse
from factory.django import DjangoModelFactory
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_product_list_empty(api_client: APIClient) -> None:
    """Test product list endpoint with no products."""
    url = reverse("products:product-list")

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 0


def test_product_list(api_client: APIClient, product_factory: DjangoModelFactory) -> None:
    """Test product list endpoint with products."""
    url = reverse("products:product-list")

    product_factory.create_batch(2)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 2


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

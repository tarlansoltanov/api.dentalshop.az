import pytest
from django.urls import reverse
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from rest_framework import status
from rest_framework.test import APIClient

from server.apps.account.models import User

pytestmark = pytest.mark.django_db


def test_category_list_empty(api_client: APIClient) -> None:
    """Test category list endpoint with no categories."""
    url = reverse("categories:category-list")

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 0


def test_category_list(api_client: APIClient, category_factory: DjangoModelFactory) -> None:
    """Test category list endpoint with categories."""
    url = reverse("categories:category-list")

    category_factory.create_batch(2, is_main=True)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 2


def test_category_list_with_children(api_client: APIClient, category_factory: DjangoModelFactory) -> None:
    """Test category list endpoint with categories and children."""
    url = reverse("categories:category-list")

    category = category_factory.create(is_main=True)
    category_factory.create_batch(2, is_main=False, parent=category)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 1
    assert len(response.data[0]["children"]) == 2


def test_category_detail_invalid_slug(api_client: APIClient) -> None:
    """Test category detail endpoint with invalid slug."""
    url = reverse("categories:category-detail", kwargs={"slug": "invalid"})

    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_category_detail_valid_slug(api_client: APIClient, category_factory: DjangoModelFactory) -> None:
    """Test category detail endpoint with valid slug."""
    category = category_factory.create()

    url = reverse("categories:category-detail", kwargs={"slug": category.slug})

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert response.data["name"] == category.name
    assert response.data["slug"] == category.slug


def test_category_create_unauthenticated(api_client: APIClient) -> None:
    """Test category create endpoint without authentication."""
    url = reverse("categories:category-list")

    data = {
        "name": "Category 1",
    }

    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_category_create_unauthorized(api_client: APIClient, user: User) -> None:
    """Test category create endpoint without correct permissions."""
    url = reverse("categories:category-list")

    data = {
        "name": "Category 1",
    }

    api_client.force_authenticate(user=user)

    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_category_create_valid(api_client: APIClient, admin_user: User) -> None:
    """Test category create endpoint with valid data and permissions."""
    url = reverse("categories:category-list")

    data = {
        "name": "Category 1",
    }

    api_client.force_authenticate(user=admin_user)

    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

    assert response.data["name"] == data["name"]
    assert response.data["slug"] == slugify(data["name"])


def test_category_update_unauthenticated(api_client: APIClient, category_factory: DjangoModelFactory) -> None:
    """Test category update endpoint without authentication."""
    category = category_factory.create()

    url = reverse("categories:category-detail", kwargs={"slug": category.slug})

    data = {
        "name": "Category 1",
    }

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_category_update_unauthorized(api_client: APIClient, category_factory: DjangoModelFactory, user: User) -> None:
    """Test category update endpoint without correct permissions."""
    category = category_factory.create()

    url = reverse("categories:category-detail", kwargs={"slug": category.slug})

    data = {
        "name": "Category 1",
    }

    api_client.force_authenticate(user=user)

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_category_update_invalid_slug(api_client: APIClient, admin_user: User) -> None:
    """Test category update endpoint with invalid slug but correct permissions."""
    url = reverse("categories:category-detail", kwargs={"slug": "invalid"})

    data = {
        "name": "Category 1",
    }

    api_client.force_authenticate(user=admin_user)

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_category_update_invalid_data(
    api_client: APIClient, category_factory: DjangoModelFactory, admin_user: User
) -> None:
    """Test category update endpoint with invalid data but correct permissions."""
    category = category_factory.create()

    url = reverse("categories:category-detail", kwargs={"slug": category.slug})

    data = {
        "name": "",
    }

    api_client.force_authenticate(user=admin_user)

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_category_update_valid(api_client: APIClient, category_factory: DjangoModelFactory, admin_user: User) -> None:
    """Test category update endpoint with valid data and permissions."""
    category = category_factory.create()

    url = reverse("categories:category-detail", kwargs={"slug": category.slug})

    data = {
        "name": "Category 1",
    }

    api_client.force_authenticate(user=admin_user)

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK

    assert response.data["name"] == data["name"]
    assert response.data["slug"] == slugify(data["name"])


def test_category_delete_unauthenticated(api_client: APIClient, category_factory: DjangoModelFactory) -> None:
    """Test category delete endpoint without authentication."""
    category = category_factory.create()

    url = reverse("categories:category-detail", kwargs={"slug": category.slug})

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_category_delete_unauthorized(api_client: APIClient, category_factory: DjangoModelFactory, user: User) -> None:
    """Test category delete endpoint without correct permissions."""
    category = category_factory.create()

    url = reverse("categories:category-detail", kwargs={"slug": category.slug})

    api_client.force_authenticate(user=user)

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_category_delete_invalid_slug(api_client: APIClient, admin_user: User) -> None:
    """Test category delete endpoint with invalid slug but correct permissions."""
    url = reverse("categories:category-detail", kwargs={"slug": "invalid"})

    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_category_delete_valid(api_client: APIClient, category_factory: DjangoModelFactory, admin_user: User) -> None:
    """Test category delete endpoint with valid data and permissions."""
    category = category_factory.create()

    url = reverse("categories:category-detail", kwargs={"slug": category.slug})

    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert response.data is None

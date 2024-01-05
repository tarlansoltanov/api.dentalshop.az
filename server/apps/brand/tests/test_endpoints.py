import pathlib
import tempfile

import pytest
from django.urls import reverse
from django.utils.text import slugify
from factory.django import DjangoModelFactory
from rest_framework import status
from rest_framework.test import APIClient

from server.apps.account.models import User

pytestmark = pytest.mark.django_db


def test_brand_list_empty(api_client: APIClient) -> None:
    """Test brand list endpoint with no brands."""
    url = reverse("brands:brand-list")

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 0


def test_brand_list(api_client: APIClient, brand_factory: DjangoModelFactory) -> None:
    """Test brand list endpoint with brands."""
    url = reverse("brands:brand-list")

    brand_factory.create_batch(2)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 2


def test_brand_detail_invalid_slug(api_client: APIClient) -> None:
    """Test brand detail endpoint with invalid slug."""
    url = reverse("brands:brand-detail", kwargs={"slug": "invalid"})

    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_brand_detail_valid_slug(api_client: APIClient, brand_factory: DjangoModelFactory) -> None:
    """Test brand detail endpoint with valid slug."""
    brand = brand_factory.create()

    url = reverse("brands:brand-detail", kwargs={"slug": brand.slug})

    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert brand.photo.url in response.data["photo"]
    assert response.data["name"] == brand.name
    assert response.data["slug"] == brand.slug


def test_brand_create_unauthenticated(api_client: APIClient) -> None:
    """Test brand create endpoint without authentication."""
    url = reverse("brands:brand-list")

    data = {
        "name": "Brand 1",
    }

    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_brand_create_unauthorized(api_client: APIClient, user: User) -> None:
    """Test brand create endpoint without correct permissions."""
    url = reverse("brands:brand-list")

    data = {
        "name": "Brand 1",
    }

    api_client.force_authenticate(user=user)

    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_brand_create_valid(api_client: APIClient, admin_user: User, temporary_image) -> None:
    """Test brand create endpoint with valid data and permissions."""
    url = reverse("brands:brand-list")

    data = {
        "photo": temporary_image,
        "name": "Brand 1",
    }

    filename = pathlib.Path(temporary_image.name).name

    api_client.force_authenticate(user=admin_user)

    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

    assert filename in response.data["photo"]
    assert response.data["name"] == data["name"]
    assert response.data["slug"] == slugify(data["name"])


def test_brand_update_unauthenticated(api_client: APIClient, brand_factory: DjangoModelFactory) -> None:
    """Test brand update endpoint without authentication."""
    brand = brand_factory.create()

    url = reverse("brands:brand-detail", kwargs={"slug": brand.slug})

    data = {
        "name": "Brand 1",
    }

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_brand_update_unauthorized(api_client: APIClient, brand_factory: DjangoModelFactory, user: User) -> None:
    """Test brand update endpoint without correct permissions."""
    brand = brand_factory.create()

    url = reverse("brands:brand-detail", kwargs={"slug": brand.slug})

    data = {
        "name": "Brand 1",
    }

    api_client.force_authenticate(user=user)

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_brand_update_invalid_slug(api_client: APIClient, brand_factory: DjangoModelFactory, admin_user: User) -> None:
    """Test brand update endpoint with invalid slug but correct permissions."""
    url = reverse("brands:brand-detail", kwargs={"slug": "invalid"})

    data = {
        "name": "Brand 1",
    }

    api_client.force_authenticate(user=admin_user)

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_brand_update_invalid_data(api_client: APIClient, brand_factory: DjangoModelFactory, admin_user: User) -> None:
    """Test brand update endpoint with invalid data but correct permissions."""
    brand = brand_factory.create()

    url = reverse("brands:brand-detail", kwargs={"slug": brand.slug})

    data = {
        "name": "",
    }

    api_client.force_authenticate(user=admin_user)

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_brand_update_valid(api_client: APIClient, brand_factory: DjangoModelFactory, admin_user: User) -> None:
    """Test brand update endpoint with valid data and permissions."""
    brand = brand_factory.create()

    url = reverse("brands:brand-detail", kwargs={"slug": brand.slug})

    data = {
        "name": "Brand 1",
    }

    api_client.force_authenticate(user=admin_user)

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK

    assert response.data["name"] == data["name"]
    assert response.data["slug"] == slugify(data["name"])


def test_brand_update_valid_with_photo(
    api_client: APIClient,
    brand_factory: DjangoModelFactory,
    admin_user: User,
    temporary_image: tempfile.NamedTemporaryFile,
) -> None:
    """Test brand update endpoint with valid data and permissions and photo."""
    brand = brand_factory.create()

    url = reverse("brands:brand-detail", kwargs={"slug": brand.slug})

    data = {
        "photo": temporary_image,
        "name": "Brand 1",
    }

    filename = pathlib.Path(temporary_image.name).name

    api_client.force_authenticate(user=admin_user)

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK

    assert filename in response.data["photo"]
    assert response.data["name"] == data["name"]
    assert response.data["slug"] == slugify(data["name"])


def test_brand_delete_unauthenticated(api_client: APIClient, brand_factory: DjangoModelFactory) -> None:
    """Test brand delete endpoint without authentication."""
    brand = brand_factory.create()

    url = reverse("brands:brand-detail", kwargs={"slug": brand.slug})

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_brand_delete_unauthorized(api_client: APIClient, brand_factory: DjangoModelFactory, user: User) -> None:
    """Test brand delete endpoint without correct permissions."""
    brand = brand_factory.create()

    url = reverse("brands:brand-detail", kwargs={"slug": brand.slug})

    api_client.force_authenticate(user=user)

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_brand_delete_invalid_slug(api_client: APIClient, admin_user: User) -> None:
    """Test brand delete endpoint with invalid slug but correct permissions."""
    url = reverse("brands:brand-detail", kwargs={"slug": "invalid"})

    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_brand_delete_valid(api_client: APIClient, brand_factory: DjangoModelFactory, admin_user: User) -> None:
    """Test brand delete endpoint with valid data and permissions."""
    brand = brand_factory.create()

    url = reverse("brands:brand-detail", kwargs={"slug": brand.slug})

    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert response.data is None

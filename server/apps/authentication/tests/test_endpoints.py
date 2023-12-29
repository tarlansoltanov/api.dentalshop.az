import pytest
from django.urls import reverse

from server.apps.account.models import User

pytestmark = pytest.mark.django_db


def test_register_with_no_data(api_client):
    """Test the register endpoint with no data."""

    endpoint = reverse("auth:register")

    response = api_client.post(endpoint, {})

    assert response.status_code == 400

    assert set(response.data.keys()) == set(
        ["first_name", "last_name", "birth_date", "phone", "password", "password_confirm"]
    )


def test_register_passwords_mismatch(api_client, user_data):
    """Test the register endpoint with passwords mismatch."""

    endpoint = reverse("auth:register")

    user_data["password_confirm"] = "mismatch"

    response = api_client.post(endpoint, user_data)

    assert response.status_code == 400

    assert response.data.keys() == set(["password_confirm"])

    assert User.objects.count() == 0


def test_register(api_client, user_data):
    """Test the register endpoint with correct data."""

    endpoint = reverse("auth:register")

    response = api_client.post(endpoint, user_data)

    assert response.status_code == 201

    assert response.data["first_name"] == user_data["first_name"]
    assert response.data["last_name"] == user_data["last_name"]
    assert response.data["phone"] == user_data["phone"]

    assert "password" not in response.data
    assert "password_confirm" not in response.data

    assert User.objects.count() == 1

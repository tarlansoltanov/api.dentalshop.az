import pytest
from rest_framework.test import APIClient

from server.apps.account.models import User


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user_data() -> dict:
    return {
        "first_name": "Test",
        "last_name": "Test",
        "birth_date": "2000-01-01",
        "phone": "500000000",
        "password": "testpassword",
        "password_confirm": "testpassword",
    }


@pytest.fixture
def user(user_data: dict) -> User:
    user_data.pop("password_confirm")
    return User.objects.create_user(**user_data)

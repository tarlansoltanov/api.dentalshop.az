import tempfile

import pytest
from django.conf import LazySettings
from PIL import Image
from rest_framework.test import APIClient

from server.apps.user.models import User


@pytest.fixture(autouse=True)
def _media_root(
    settings: LazySettings,
    tmpdir_factory: pytest.TempPathFactory,
) -> None:
    """Forces django to save media files into temp folder."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp("media", numbered=True)


@pytest.fixture
def temporary_image() -> tempfile.NamedTemporaryFile:
    """Returns path to temporary image."""
    image = Image.new("RGB", (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file


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

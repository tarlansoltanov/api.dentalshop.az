import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_health_check(client):
    response = client.get("/health/?format=json")
    assert response.status_code == 200


def test_robot_txt(client):
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response["Content-Type"] == "text/plain"
    assert response.content == b"User-agent: *\nDisallow:\n"


def test_swagger(api_client):
    response = api_client.get(reverse("schema-swagger-ui"))
    assert response.status_code == 200
    assert response["Content-Type"] == "text/html; charset=utf-8"

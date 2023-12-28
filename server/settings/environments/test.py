"""Test Environment Settings."""

from server.settings.components.common import INSTALLED_APPS

SECRET_KEY = "django-insecure-1&*3v*eb087ef-ah5c$&o"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    "server.apps.core.tests",
]

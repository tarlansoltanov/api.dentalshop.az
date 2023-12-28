# Django Health Check
# https://django-health-check.readthedocs.io/en/latest/

from server.settings.components.common import INSTALLED_APPS

INSTALLED_APPS += [
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.migrations",
]

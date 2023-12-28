"""
Django Project - Settings Module.

This module is responsible for loading the all component setting files and
correct settings file based on the environment variable DJANGO_ENV.
The default value is 'local', so if you don't specify
the environment variable, the local settings will be loaded.

For more information, see the documentation:
https://django-split-settings.readthedocs.io/en/latest/
"""

from split_settings.tools import include

from server.settings.components import config

ENV = config("DJANGO_ENV", default="local") or "local"

base_settings = (
    "components/common.py",  # Standard Django Settings.
    "components/database.py",  # Database configuration.
    "components/logging.py",  # Logging configuration.
    "components/healthcheck.py",  # Health checks.
    "components/cors.py",  # CORS configuration.
    "components/restframework.py",  # Django REST Framework.
    "components/custom.py",  # Custom Project Settings.
    f"environments/{ENV}.py",  # Environment settings.
)

include(*base_settings)

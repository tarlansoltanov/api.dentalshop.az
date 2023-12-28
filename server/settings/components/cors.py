# Django CORS Headers
# https://github.com/adamchainz/django-cors-headers

from server.settings.components.common import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS += ["corsheaders"]

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")

CORS_ORIGIN_ALLOW_ALL = True

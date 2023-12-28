"""Production environment settings."""

from server.settings.components import BASE_DIR, config

SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    config("DOMAIN_NAME"),
    config("DOMAIN_IP"),
    # We need this value for `healthcheck` to work:
    "localhost",
]

IN_DOCKER = config("IN_DOCKER", cast=bool, default=False)

# Staticfiles
# https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/

STATIC_ROOT = "/var/www/static" if IN_DOCKER else BASE_DIR / "staticfiles"

# Media files
# https://docs.djangoproject.com/en/5.0/topics/files/

MEDIA_ROOT = "/var/www/media" if IN_DOCKER else BASE_DIR / "media"

# Security
# https://docs.djangoproject.com/en/5.0/topics/security/

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = [
    # This is required for healthcheck to work:
    "^health/",
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

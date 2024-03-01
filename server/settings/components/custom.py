# Custom Project Settings

from server.settings.components import BASE_DIR
from server.settings.components.common import INSTALLED_APPS

# Application definition

INSTALLED_APPS += [
    "server.apps.core",
    "server.apps.auth",
    "server.apps.user",
    "server.apps.account",
    "server.apps.brand",
    "server.apps.category",
    "server.apps.product",
    "server.apps.freezone",
    "server.apps.order",
    "server.apps.banner",
    "server.apps.notification",
]

# Modeltranslation
# https://django-modeltranslation.readthedocs.io/en/latest/

MODELTRANSLATION_TRANSLATION_FILES = [
    "server.apps.brand.logic.translation",
    "server.apps.category.logic.translation",
    "server.apps.product.logic.translation",
]

# Media files
# https://docs.djangoproject.com/en/4.2/topics/files/

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

# Custom User Model

AUTH_USER_MODEL = "user.User"

# Custom Project Settings

from server.settings.components.common import INSTALLED_APPS

INSTALLED_APPS += [
    "server.apps.core",
    "server.apps.authentication",
    "server.apps.account",
]

# Custom User Model

AUTH_USER_MODEL = "account.User"

from django.contrib import admin
from solo.admin import SingletonModelAdmin

from server.apps.config.models import AppVersionConfiguration

admin.site.register(AppVersionConfiguration, SingletonModelAdmin)

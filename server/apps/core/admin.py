from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from server.apps.core.constants import API_PREFIX
from server.settings.components import config

PROJECT_NAME = config("PROJECT_NAME", default="Project", cast=str).capitalize()

# Text to put at the end of each page's <title>.
admin.site.site_title = "CodeShift Admin"

# Text to put in each page's <div id="site-name">.
admin.site.site_header = "CodeShift Admin"

# Text to put at the top of the admin index page.
admin.site.index_title = f'{PROJECT_NAME} {_("Site administration")}'

# URL for the "View site" link at the top of each admin page.
admin.site.site_url = f"/{API_PREFIX}"

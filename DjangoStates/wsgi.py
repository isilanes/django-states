# Standard libs:
import os

# Django libs:
from django.core.wsgi import get_wsgi_application


# Code:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoStates.settings")
application = get_wsgi_application()

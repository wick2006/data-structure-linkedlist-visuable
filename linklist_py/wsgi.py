# linklist_py/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linklist_py.settings")

application = get_wsgi_application()

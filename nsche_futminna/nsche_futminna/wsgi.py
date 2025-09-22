"""
WSGI config for nsche_futminna project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nsche_futminna.settings")

application = get_wsgi_application()
import sys
import os

path = '/home/nschefutminna/nsche_futminna'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'nsche_futminna.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

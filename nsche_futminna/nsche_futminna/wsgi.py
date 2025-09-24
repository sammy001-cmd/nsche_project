"""
WSGI config for nsche_futminna project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# Add project path
path = '/home/nschefutminna/nsche_project/nsche_futminna'
if path not in sys.path:
    sys.path.append(path)

# Set the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'nsche_futminna.settings'

# Activate virtualenv
activate_this = '/home/nschefutminna/.virtualenvs/nscheenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



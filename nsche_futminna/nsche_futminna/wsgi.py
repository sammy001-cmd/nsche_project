"""
WSGI config for nsche_futminna project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# Add both project and app paths
project_home = '/home/nschefutminna/nsche_project'
if project_home not in sys.path:
    sys.path.append(project_home)

# Set environment variable for settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'nsche_futminna.settings'

# Activate the correct virtualenv
activate_this = '/home/nschefutminna/.virtualenvs/nscheenv39/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()



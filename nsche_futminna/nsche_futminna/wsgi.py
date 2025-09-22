"""
WSGI config for nsche_futminna project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# add your project directory to the sys.path
project_home = '/NSCHFUTMINNA/nsche_futminna/nsche_futminna'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# activate virtualenv
activate_this = '/NSCHFUTMINNA/nsche_futminna/nsche_futminna/venv/bin/activate_this.py'
if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nsche_futminna.settings')
# optionally set SECRET_KEY here (temporary; better to store securely)
# os.environ['DJANGO_SECRET_KEY'] = 'your-secret-key'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

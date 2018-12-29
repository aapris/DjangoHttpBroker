"""
WSGI config for plugindemo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from businesslogic.setup import import_plugins

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plugindemo.settings')

import_plugins()

application = get_wsgi_application()

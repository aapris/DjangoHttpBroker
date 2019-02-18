from .celery import app as celery_app
from broker.setup import import_plugins
# To avoid `django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.`
# while loading plugins dynamiocally, keep these lines here:
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

__all__ = ('celery_app',)

import_plugins()

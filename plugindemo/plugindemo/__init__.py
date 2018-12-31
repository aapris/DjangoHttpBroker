from .celery import app as celery_app
from businesslogic.setup import import_plugins

__all__ = ('celery_app',)

import_plugins()

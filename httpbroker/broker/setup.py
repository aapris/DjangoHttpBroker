from django.conf import settings
from django.utils.module_loading import import_module


def import_plugins():
    """
    Import all plugin modules and initialise EndpointProvider instances found.
    """
    apps = []

    for appname in settings.INSTALLED_APPS:
        if appname.startswith('django.') is False:
            try:
                apps.append(import_module(appname + '.endpoints'))
            except ModuleNotFoundError:
                pass
            try:
                apps.append(import_module(appname + '.forwards'))
            except ModuleNotFoundError:
                pass
            try:
                apps.append(import_module(appname + '.decoders'))
            except ModuleNotFoundError:
                pass

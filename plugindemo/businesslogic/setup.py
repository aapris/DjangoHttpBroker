from django.conf import settings
from django.utils.module_loading import import_module
from businesslogic.endpoint import EndpointProvider
from businesslogic.endpoint import ForwardProvider


def import_plugins():
    """
    Import all plugin modules and initialise EndpointProvider instances found.
    """
    apps = []
    print('Loading endpoints...')

    for appname in settings.INSTALLED_APPS:
        if appname.startswith('django.') is False:
            print(f'{appname}: ', end='')
            try:
                apps.append(import_module(appname + '.endpoints'))
                print('endpoints found!')
            except ModuleNotFoundError as err:
                print(err)
            try:
                apps.append(import_module(appname + '.forwards'))
                print('forwards found!')
            except ModuleNotFoundError as err:
                print(err)

        endpoints = EndpointProvider.get_plugins()
        for e in endpoints:
            print(f'{e.name}: {e.description}')

        forwards = ForwardProvider.get_plugins()
        for f in forwards:
            print(f'{f.name}: {f.description}')

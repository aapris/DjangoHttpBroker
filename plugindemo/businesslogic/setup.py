from django.conf import settings
from django.utils.module_loading import import_module
from businesslogic.endpoint import EndpointProvider


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
                print(' endpoints found!')
            except ModuleNotFoundError as err:
                print(err)

        actions = EndpointProvider.get_plugins()
        for a in actions:
            print(f'{a.name}: {a.description}')

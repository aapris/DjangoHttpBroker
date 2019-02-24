from django.conf import settings
from django.utils.module_loading import import_module


def import_plugins():
    """
    Import all plugin modules and initialise EndpointProvider instances found.
    """
    apps = []
    # print('Loading endpoints...')

    for appname in settings.INSTALLED_APPS:
        if appname.startswith('django.') is False:
            # print(f'{appname}: ', end='')
            try:
                apps.append(import_module(appname + '.endpoints'))
                # print(f'{appname} endpoints found!')
            except ModuleNotFoundError as err:
                pass
                # print(err)
            try:
                apps.append(import_module(appname + '.forwards'))
                # print(f'{appname} forwards found!')
            except ModuleNotFoundError as err:
                pass
                # print(err)
            try:
                apps.append(import_module(appname + '.decoders'))
                # print(f'{appname} decoders found!')
            except ModuleNotFoundError as err:
                pass
                # print(err)

        # endpoints = EndpointProvider.get_plugins()
        # for e in endpoints:
        #     print(f'{e.name}: {e.description}')
        #
        # forwards = ForwardProvider.get_plugins()
        # for f in forwards:
        #     print(f'{f.name}: {f.description}')

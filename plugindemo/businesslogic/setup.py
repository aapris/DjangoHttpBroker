# This initialises plugin, but is hard coded.
# Something like this may be a solution:
# https://eldarion.com/blog/2013/02/14/entry-point-hook-django-projects/
# action = importlib.import_module('actions.' + action)
# from builtinplugin.plugins import BuiltinApp1

from django.conf import settings
from django.utils.module_loading import import_module

def import_plugins():
    apps = []
    for appname in settings.INSTALLED_APPS:
        if appname.startswith('django.') is False:
            print(appname + ': ', end='')
            try:
                apps.append(import_module(appname + '.plugins'))
                # apps.append(import_module(appname + '.plugins.plugari1'))
                print("OK")
                # print(apps[-1])
            except ModuleNotFoundError as err:
                print(err)
        from businesslogic.plugin import EndpointProvider
        actions = EndpointProvider.get_plugins()
        for a in actions:
            print(a.title, a.description)
        print(actions)
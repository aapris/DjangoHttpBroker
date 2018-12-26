from django.urls import reverse
from django.http.response import HttpResponse


class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)

    def get_plugins(cls, *args, **kwargs):
        return [p(*args, **kwargs) for p in cls.plugins]


class EndpointProvider(object, metaclass=PluginMount):
    """
    Mount point for plugins which refer to actions that can be performed.

    Plugins implementing this reference should provide the following attributes:

    ========  ========================================================
    title     The text to be displayed, describing the action

    url       The URL to the view where the action will be carried out

    selected  Boolean indicating whether the action is the one
              currently being performed
    ========  ========================================================
    """

    # __metaclass__ = PluginMount

    def __init__(self, request=None, *args, **kwargs):
        pass
        # self.url = reverse(self.view, args=args, kwargs=kwargs)
        # self.selected = request.META['PATH_INFO'] == self.url


# Plugins below should be appname/plugins.py or appname/plugins/someplugin.py or something
# and they should get automatically initialised (but they won't yet)


class BuiltinEndpoint1(EndpointProvider):
    title = 'BuiltinEndpoint1'
    description = '1st endpoint handler'

    def handle_request(self, request):
        return HttpResponse('OK', content_type='text/plain')


class BuiltinEndpoint2(EndpointProvider):
    title = 'BuiltinEndpoint2'
    description = '2nd endpoint handler'

    def handle_request(self, request):
        return HttpResponse('$OK$', content_type='text/plain')

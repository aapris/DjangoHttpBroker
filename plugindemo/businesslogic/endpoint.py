"""
The root of "Simple Plugin Framework" can be found from here:
http://martyalchin.com/2008/jan/10/simple-plugin-framework/
"""

class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where endpoints can be registered later.
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
    Mount point for endpoints which refer to actions that can be performed.

    Plugins implementing this reference should provide the following attributes:

    ===========  ========================================================
    name         Unique name for handler

    app          Namespace for endpoints

    description  Human readable description
    ===========  ========================================================
    """

    def __init__(self, request=None, *args, **kwargs):
        """
        Set initially name from class name and
        namespace / app from module name (Django application name).
        Description is set by implementation.
        """
        self.name = type(self).__name__
        self.app = type(self).__module__.split('.')[0]

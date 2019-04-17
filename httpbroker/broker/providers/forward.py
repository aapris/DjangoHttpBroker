import sys
import inspect
import pkgutil
from pathlib import Path
from importlib import import_module
from . import PluginMount


class ForwardProvider(object, metaclass=PluginMount):
    """
    Mount point for endpoints which refer to actions that can be performed.

    Plugins implementing this reference should provide the following attributes:

    ===========  ========================================================
    name         Unique name for handler

    app          Namespace for forwards

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
        self.full_name = f'{self.app}.{self.name}'

    # TODO:
    # def forward_data() abstract method


def import_forwards(_file, _name):
    """
    Load all ForwardProvider instances in current module dir
    :param _file:  always __file__
    :param _name: always __name__
    """
    for (_, name, _) in pkgutil.iter_modules([Path(_file).parent]):
        imported_module = import_module('.' + name, package=_name)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if inspect.isclass(attribute) and issubclass(attribute, ForwardProvider):
                setattr(sys.modules[__name__], name, attribute)

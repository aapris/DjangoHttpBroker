# __all__ = ['plugari1', ]

from businesslogic.plugin import EndpointProvider
from pathlib import Path
import sys
import inspect
import pkgutil
from importlib import import_module


for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):

    imported_module = import_module('.' + name, package=__name__)

    for i in dir(imported_module):
        attribute = getattr(imported_module, i)

        if inspect.isclass(attribute) and issubclass(attribute, EndpointProvider):
            setattr(sys.modules[__name__], name, attribute)
#!/usr/bin/env python
import os
import sys
# This initialises plugin, but is hard coded.
# Something like this may be a solution:
# https://eldarion.com/blog/2013/02/14/entry-point-hook-django-projects/
from builtinplugin.plugins import BuiltinApp1

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plugindemo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

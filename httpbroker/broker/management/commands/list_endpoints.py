import json
from django.core.management.base import BaseCommand, CommandError
from broker.models import Endpoint, Forward
from broker.endpoint import EndpointProvider, ForwardProvider


class Command(BaseCommand):
    help = 'List all configured Endpoints'

    def add_arguments(self, parser):
        # parser.add_argument('keys', nargs='+', type=str)
        pass

    def handle(self, *args, **options):
        print('Available Endpoints\n=========================')
        endpoints = EndpointProvider.get_plugins()
        for a in endpoints:
            name = f'{a.app}.{a.name}'
            print(f'{name: <40}{a.description}')
        print('\nConfigured Endpoints\n=========================')
        for e in Endpoint.objects.all():
            print(f'{e.handler: <40}/{e.path}')

        print('\nAvailable Forwards\n=========================')
        forwards = ForwardProvider.get_plugins()
        # forwards.sort()
        for a in forwards:
            name = f'{a.app}.{a.name}'
            print(f'{name: <40}{a.description}')
        print('\nConfigured Forwards\n=========================')
        for e in Forward.objects.all():
            config = json.dumps(json.loads(e.config))
            print(f'{e.handler: <40}{config}')

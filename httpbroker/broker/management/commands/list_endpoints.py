import json
from django.core.management.base import BaseCommand, CommandError
from broker.models import Endpoint, Forward, Decoder
from broker.providers.endpoint import EndpointProvider
from broker.providers.forward import ForwardProvider
from broker.providers.decoder import DecoderProvider


class Command(BaseCommand):
    help = 'List all configured Endpoints'

    def add_arguments(self, parser):
        # parser.add_argument('keys', nargs='+', type=str)
        pass

    def handle(self, *args, **options):
        print('Available Endpoints\n=========================')
        endpoints = EndpointProvider.get_plugins()
        for a in endpoints:
            print(f'{a.full_name: <40}{a.description}')
        print('\nConfigured Endpoints\n=========================')
        for e in Endpoint.objects.all():
            print(f'{e.handler: <40}/{e.path}')

        print('\nAvailable Forwards\n=========================')
        forwards = ForwardProvider.get_plugins()
        # forwards.sort()
        for a in forwards:
            print(f'{a.full_name: <40}{a.description}')
        print('\nConfigured Forwards\n=========================')
        for e in Forward.objects.all():
            config = json.dumps(json.loads(e.config))
            print(f'{e.handler: <40}{config}')

        print('\nAvailable Decoders\n=========================')
        decoders = DecoderProvider.get_plugins()
        for a in decoders:
            print(f'{a.full_name: <40}{a.description}')
        print('\nConfigured Decoders\n=========================')
        for e in Decoder.objects.all():
            config = json.dumps(json.loads(e.config))
            print(f'{e.handler: <40}{config}')

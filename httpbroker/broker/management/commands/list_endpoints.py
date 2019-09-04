import json
from django.core.management.base import BaseCommand
from broker.models import Endpoint, Forward, Decoder
from broker.providers.endpoint import EndpointProvider
from broker.providers.forward import ForwardProvider
from broker.providers.decoder import DecoderProvider


class Command(BaseCommand):
    help = 'List all configured Endpoints'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('Available Endpoints\n=========================')
        endpoints = EndpointProvider.get_plugins()
        for a in endpoints:
            self.stdout.write(f'{a.full_name: <40}{a.description}')
        self.stdout.write('\nConfigured Endpoints\n=========================')
        for e in Endpoint.objects.all():
            self.stdout.write(f'{e.handler: <40}/{e.path}')

        self.stdout.write('\nAvailable Forwards\n=========================')
        forwards = ForwardProvider.get_plugins()
        for a in forwards:
            self.stdout.write(f'{a.full_name: <40}{a.description}')
        self.stdout.write('\nConfigured Forwards\n=========================')
        for e in Forward.objects.all():
            config = json.dumps(json.loads(e.config))
            self.stdout.write(f'{e.handler: <40}{config}')

        self.stdout.write('\nAvailable Decoders\n=========================')
        decoders = DecoderProvider.get_plugins()
        for a in decoders:
            self.stdout.write(f'{a.full_name: <40}{a.description}')
        self.stdout.write('\nConfigured Decoders\n=========================')
        for e in Decoder.objects.all():
            config = json.dumps(json.loads(e.config))
            self.stdout.write(f'{e.handler: <40}{config}')

from django.core.management.base import BaseCommand, CommandError
from broker.models import Endpoint


class Command(BaseCommand):
    help = 'List all configured Endpoints'

    def add_arguments(self, parser):
        # parser.add_argument('keys', nargs='+', type=str)
        pass

    def handle(self, *args, **options):
        for e in Endpoint.objects.all():
            print(f'/{e.path}')

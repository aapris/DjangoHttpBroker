import os
import datetime
from django.conf import settings
from broker.management.commands import RabbitCommand
from broker.utils import data_unpack


def consumer_callback(channel, method, properties, body):
    data = data_unpack(body)
    print(data)
    # channel.basic_ack(method.delivery_tag)


class Command(RabbitCommand):
    help = 'Read RabbitMQ queue and save all data into InfluxDB'

    def add_arguments(self, parser):
        # parser.add_argument('keys', nargs='+', type=str)
        super().add_arguments(parser)
        pass

    def handle(self, *args, **options):
        options['exchange'] = settings.PARSED_DATA_EXCHANGE
        options['queue'] = 'save2influxdb_queue'
        options['routing_key'] = f'{settings.RABBITMQ["ROUTING_KEY_PREFIX"]}.#'
        options['consumer_callback'] = consumer_callback
        super().handle(*args, **options)

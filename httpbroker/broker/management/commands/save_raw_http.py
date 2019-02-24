import os
import datetime
from django.conf import settings
from broker.management.commands import RabbitCommand

RAW_HTTP_EXCHANGE = 'incoming_raw_http'


def consumer_callback(channel, method, properties, body):
    # Construct filename
    fname = f'{method.routing_key}.msgpack'
    date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    path = os.path.join(settings.VAR_DIR, 'httprequests', date)
    fpath = os.path.join(path, fname)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(fpath, 'ab') as f:
        f.write(body)
    print(f'Successfully saved message {method.delivery_tag}')
    channel.basic_ack(method.delivery_tag)


class Command(RabbitCommand):
    help = 'Read RabbitMQ queue and save all messages to a file'

    def add_arguments(self, parser):
        # parser.add_argument('keys', nargs='+', type=str)
        super().add_arguments(parser)
        pass

    def handle(self, *args, **options):
        options['routing_key'] = f'{settings.RABBITMQ["ROUTING_KEY_PREFIX"]}.#'
        options['queue_name'] = 'raw_http_save_queue'
        options['consumer_callback'] = consumer_callback
        super().handle(*args, **options)

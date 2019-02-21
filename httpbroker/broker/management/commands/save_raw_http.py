import os
import datetime
import time
import pika
import pika.exceptions
from dateutil.parser import parse
from django.conf import settings
from django.core.management.base import BaseCommand
from broker.utils import data_unpack

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


class Command(BaseCommand):
    help = 'Read RabbitMQ queue and save all messages to a file'

    def add_arguments(self, parser):
        # TODO: add arguments for file path, routing_key etc.
        # parser.add_argument('keys', nargs='+', type=str)
        pass

    def handle(self, *args, **options):
        conn_params = pika.ConnectionParameters('localhost', 5672, '/',
                                                #  pika.credentials.PlainCredentials('user', 'password')
                                                )
        try:
            connection = pika.BlockingConnection(conn_params)
        except pika.exceptions.ConnectionClosed as err:
            print(f'Connection failed {err}')
            exit(1)

        queue_name = 'raw_http_save_queue'
        channel = connection.channel()
        channel.queue_declare(queue_name, durable=True)
        channel.queue_bind(queue=queue_name, exchange=RAW_HTTP_EXCHANGE, routing_key='fvh.#')
        channel.basic_consume(consumer_callback, queue_name)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print('\nUser exit, bye!')
        channel.close()
        connection.close()

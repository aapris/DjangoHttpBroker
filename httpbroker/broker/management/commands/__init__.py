import functools
import pika
import pika.exceptions
from django.conf import settings
from django.core.management.base import BaseCommand


class RabbitCommand(BaseCommand):
    help = 'Base Command for all RabbitMQ Commands. Inherit this in app commands'

    def add_arguments(self, parser):
        # TODO: add arguments for file path, routing_key etc.
        # parser.add_argument('keys', nargs='+', type=str)
        pass

    def handle(self, *args, **options):
        if settings.RABBITMQ.get('USER') is not None and settings.RABBITMQ.get('PASSWORD') is not None:
            credentials = pika.PlainCredentials(settings.RABBITMQ['USER'], settings.RABBITMQ['PASSWORD'])
            conn_params = pika.ConnectionParameters('localhost', 5672, '/', credentials)
        else:
            conn_params = pika.ConnectionParameters('localhost', 5672, '/')
        try:
            connection = pika.BlockingConnection(conn_params)
        except pika.exceptions.ConnectionClosed as err:
            print(f'Connection failed: {err}')
            raise

        exchange = options['exchange']
        queue = options['queue']
        routing_key = options['routing_key']
        callback = options.pop('consumer_callback')
        channel = connection.channel()
        channel.queue_declare(queue, durable=True)
        channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)
        # Pass options to callback
        callback = functools.partial(callback, options=options)
        channel.basic_consume(queue, callback)
        print(f'Start listening {routing_key}')
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print('\nUser exit, bye!')
        channel.close()
        connection.close()

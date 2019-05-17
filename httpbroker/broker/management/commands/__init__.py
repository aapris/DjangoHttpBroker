import functools
import logging

from django.core.management.base import BaseCommand

from broker.utils import get_rabbitmq_connection

logger = logging.getLogger('broker')


class RabbitCommand(BaseCommand):
    help = 'Base Command for all RabbitMQ Commands. Inherit this in app commands'

    def add_arguments(self, parser):
        # TODO: add arguments for file path, routing_key etc.
        parser.add_argument("-l", "--log", dest="log", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                            help="Set the logging level")

    def handle(self, *args, **options):
        if options['log'] is not None:
            logging.getLogger().setLevel(options['log'])
        connection = get_rabbitmq_connection()

        # These must always be present
        exchange = options['exchange']
        queue = options['queue']
        callback = options.pop('consumer_callback')
        # Routing key and arguments are alternate
        routing_key = options.get('routing_key', '')
        arguments = options.get('arguments')
        # Build bind_args to pass to queue_bind()
        bind_args = {
            'queue': queue,
            'exchange': exchange,
        }
        # If arguments (=headers) are present, we are listening to Headers Exchange and routing_key is empty
        if arguments is not None:
            bind_args['arguments'] = arguments
            bind_args['routing_key'] = ''
        else:
            bind_args['routing_key'] = routing_key
        # Create channel, declare queue and bind it to an exchange
        channel = connection.channel()
        channel.queue_declare(queue, durable=True)
        channel.queue_bind(**bind_args)
        # Pass options to callback
        callback = functools.partial(callback, options=options)
        channel.basic_consume(queue, callback)
        log_msg = f'Start listening {bind_args}'
        logger.info(log_msg)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print('\nUser exit, bye!')
        channel.close()
        connection.close()

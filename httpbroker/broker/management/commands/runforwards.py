import json
import logging

from django.conf import settings

from broker.management.commands import RabbitCommand
from broker.providers.forward import ForwardProvider
from broker.utils import data_unpack, get_datalogger

logger = logging.getLogger('runforwards')


def consumer_callback(channel, method, properties, body, options=None):
    """
    Run all Forward plugins, one by one, defined for this Datalogger.
    """
    parsed_data = data_unpack(body)
    devid = parsed_data['devid']
    logger.debug(f'Handling {devid}')
    datalogger, created = get_datalogger(devid=devid, update_activity=False)
    dataloggerforwards = datalogger.dataloggerforwards.all()
    plugins = ForwardProvider.get_plugins({})

    for dlf in dataloggerforwards:
        # Read Forward instance's config
        f_config = json.loads(dlf.forward.config)
        # Read logger's DataForward instance's config
        config = json.loads(dlf.config)
        # Override fields defined in DataloggerForward's config
        f_config.update(config)
        # Find correct plugin and call its forward_data() function
        for plugin in plugins:
            if plugin.full_name == dlf.forward.handler:
                logger.debug(f'Using {dlf.forward.handler} ({dlf.forward.name}) for {devid}')
                success = plugin.forward_data(datalogger, parsed_data, f_config)
                if success:
                    logger.info(f'Successfully ran Forward: {dlf.forward.handler} ({dlf.forward.name}) for {devid}')
                else:
                    logger.warning(f'Forward failed to run: {dlf.forward.handler} ({dlf.forward.name}) for {devid}')
    channel.basic_ack(method.delivery_tag)


class Command(RabbitCommand):
    help = 'Read RabbitMQ queue and save all data into InfluxDB'

    def add_arguments(self, parser):
        parser.add_argument('--prefix', type=str,
                            help='queue and routing_key prefix, overrides settings.ROUTING_KEY_PREFIX')
        super().add_arguments(parser)

    def handle(self, *args, **options):
        logger.info(f'Start handling {__name__}')
        name = 'runforwards'
        # FIXME: constructing options should be (probably) in a function in broker.utils
        if options["prefix"] is None:
            prefix = settings.RABBITMQ["ROUTING_KEY_PREFIX"]
        else:
            prefix = options["prefix"]
        options['exchange'] = settings.PARSED_DATA_EXCHANGE
        options['routing_key'] = f'{prefix}.#'  # We want to catch all messages in this handler
        options['queue'] = f'{prefix}_{name}_queue'
        options['consumer_callback'] = consumer_callback
        super().handle(*args, **options)

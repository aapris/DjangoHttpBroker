import json
import logging
from django.conf import settings
from influxdb.exceptions import InfluxDBClientError
from broker.management.commands import RabbitCommand
from broker.utils import data_unpack, get_datalogger
from broker.utils.influxdb import get_influxdb_client, create_influxdb_objects

logger = logging.getLogger('django')


def datalogger_get_config(datalogger, parsed_data):
    config = {}
    if datalogger.application:
        config.update(json.loads(datalogger.application.config))
    return config


def consumer_callback(channel, method, properties, body, options=None):
    """
    Extract data from RabbitMQ message's body and save sensor values into InfluxDB
    """
    parsed_data = data_unpack(body)
    devid = parsed_data['devid']
    logger.debug(f'Handling {devid}')
    datalogger, created = get_datalogger(devid=devid, update_activity=False)
    # FIXME: think config overloading carefully
    config = datalogger_get_config(datalogger, parsed_data)
    # FIXME: 'influxdb_database' may be defined in parsed_data['config'] already!?
    dbname = config.get('influxdb_database')
    measurement_name = config.get('influxdb_measurement')
    if dbname is not None and measurement_name is not None:
        measurements = create_influxdb_objects(parsed_data, measurement_name)
        logger.debug(json.dumps(measurements))
        iclient = get_influxdb_client(database=dbname)
        iclient.create_database(dbname)
        try:
            iclient.write_points(measurements)
        except InfluxDBClientError as err:
            err_msg = f'InfluxDB error: {err}'
            logger.error(f'devid={devid} {err_msg}')
        logger.debug(json.dumps(measurements, indent=1))
    else:
        logger.warning(
            f'devid={devid} InfluxDB dbname was not found in Dataforward config. Data was not saved into InfluxDB.')
    channel.basic_ack(method.delivery_tag)


class Command(RabbitCommand):
    help = 'Read RabbitMQ queue and save all data into InfluxDB'

    def add_arguments(self, parser):
        # parser.add_argument('keys', nargs='+', type=str)
        super().add_arguments(parser)

    def handle(self, *args, **options):
        logger.info(f'Start handling {__name__}')
        options['exchange'] = settings.PARSED_DATA_HEADERS_EXCHANGE
        options['queue'] = 'save2influxdb_queue'
        options['routing_key'] = ''
        # Create queue which subscribes all messages having header 'influxdb': '1'
        options['arguments'] = {'influxdb': '1', 'x-match': 'any'}
        # logger.info(options)
        options['consumer_callback'] = consumer_callback
        super().handle(*args, **options)

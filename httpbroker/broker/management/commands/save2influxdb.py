import json
import influxdb
import logging
from django.conf import settings
from influxdb.exceptions import InfluxDBClientError
from broker.management.commands import RabbitCommand
from broker.utils import data_unpack, get_datalogger

logger = logging.getLogger('django')


def get_influxdb_client(host='127.0.0.1', port=8086, database='mydb'):
    iclient = influxdb.InfluxDBClient(host=host, port=port, database=database)
    return iclient


def create_influxdb_objects(data, measurement_name, extratags=None):
    """
    data =
    {
        "devid": "373773207E33011C",
        "datalines": [
            {
                "time": "2019-03-11T12:49:09.239162+00:00",
                "data": {
                    'pm25min': 0.2, 'pm25max': 0.3, 'pm25avg': 0.2, 'pm25med': 0.2,
                    'pm10min': 0.2, 'pm10max': 1.3, 'pm10avg': 0.7, 'pm10med': 0.6,
                    'temp': 22.5, 'humi': 22.0, 'pres': 1021.6, 'gas': 826.6,
                    'rssi': '-81.000000'
                }
            }
        ]
    }
    :param dict data: Data object, see example above
    :param str measurement_name: Measurement's name
    :param dict extratags: Additional InfluxDB measurement tags
    :return:
    """
    devid = data['devid']
    measurements = []
    for d in data['datalines']:
        measurement_obj = {
            "measurement": measurement_name,
            "tags": {
                "dev-id": devid,
            },
            "time": d['time'],
            "fields": d['data']
        }
        if extratags is not None:
            measurement_obj['tags'].update(extratags)
        measurements.append(measurement_obj)
    return measurements


def consumer_callback(channel, method, properties, body, options=None):
    """
    Extract data from RabbitMQ message's body and save sensor values into InfluxDB
    """
    parsed_data = data_unpack(body)
    devid = parsed_data['devid']
    logger.debug(f'Handling {devid}')
    datalogger, created = get_datalogger(devid=devid, update_activity=False)
    # Check if this logger has InfluxDB forward
    dataloggerforwards = datalogger.dataloggerforwards.filter(forward__handler='broker.InfluxDBForward')
    if dataloggerforwards:
        config = json.loads(dataloggerforwards[0].config)
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
        else:
            logger.warning(
                f'devid={devid} InfluxDB dbname was not found in Dataforward config. Data was not saved into InfluxDB.')
    else:
        logger.info(f'devid={devid} No forward to InfluxDB')
    channel.basic_ack(method.delivery_tag)


class Command(RabbitCommand):
    help = 'Read RabbitMQ queue and save all data into InfluxDB'

    def add_arguments(self, parser):
        # parser.add_argument('keys', nargs='+', type=str)
        super().add_arguments(parser)

    def handle(self, *args, **options):
        logger.info(f'Start handling {__name__}')
        options['exchange'] = settings.PARSED_DATA_EXCHANGE
        options['queue'] = 'save2influxdb_queue'
        options['routing_key'] = f'{settings.RABBITMQ["ROUTING_KEY_PREFIX"]}.#'
        options['consumer_callback'] = consumer_callback
        super().handle(*args, **options)

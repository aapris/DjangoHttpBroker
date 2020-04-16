import json
import logging

import influxdb
from influxdb.exceptions import InfluxDBClientError

logger = logging.getLogger('django')


def get_influxdb_client(host='127.0.0.1', port=8086, database='mydb'):
    iclient = influxdb.InfluxDBClient(host=host, port=port, database=database)
    return iclient


def create_influxdb_objects(data, measurement_name, extratags=None):
    """
    Convert a "parsed data object" (example below) to an InfluxDB object.

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
    :return: InfluxDB measurement object
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
        if extratags is not None:  # can be an argument in function call
            measurement_obj['tags'].update(extratags)
        if 'extratags' in d:  # can be in every dataline
            measurement_obj['tags'].update(d['extratags'])
        measurements.append(measurement_obj)
    return measurements


def save_parsed_data2influxdb(db_name, measurement_name, parsed_data):
    devid = parsed_data['devid']
    measurements = create_influxdb_objects(parsed_data, measurement_name)
    logger.debug(json.dumps(measurements))
    iclient = get_influxdb_client(database=db_name)
    if not any(db['name'] == db_name for db in iclient.get_list_database()):
        iclient.create_database(db_name)
    try:
        iclient.write_points(measurements)
    except InfluxDBClientError as err:
        err_msg = f'InfluxDB error: {err}'
        logger.error(f'devid={devid} {err_msg}')

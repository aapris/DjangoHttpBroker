from influxdb.exceptions import InfluxDBClientError
from dateutil.parser import parse
from broker.providers.forward import ForwardProvider
from thingpark.utils import create_influxdb_obj, get_influxdb_client


class InfluxDBForward(ForwardProvider):
    description = 'Forward data into InfluxDB'

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def forward_data(self, datalogger, data, config):
        """
        Insert parsed data into InfluxDB database.
        influxdb_measurement and influxdb_database MUST be defined in Forward's or DataloggerForward's config.
        
        :param Datalogger datalogger:
        :param dict data:
        :param dict config:
        :return: True on success, False if writing data failed
        """
        measurement_name = config['influxdb_measurement']
        dbname = config['influxdb_database']
        measurements = []
        for dataline in data['datalines']:
            ts = parse(dataline['time'])
            measurement = create_influxdb_obj(datalogger.devid, measurement_name, dataline['data'], ts)
            measurements.append(measurement)
        iclient = get_influxdb_client(database=dbname)
        iclient.create_database(dbname)
        try:
            iclient.write_points(measurements)
        except InfluxDBClientError as err:
            return False
        return True

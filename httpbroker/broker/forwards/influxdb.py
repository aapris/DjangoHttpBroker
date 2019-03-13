from broker.providers.forward import ForwardProvider


class InfluxDBForward(ForwardProvider):
    description = 'Forward data into InfluxDB'

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def forward_data(self, data):
        # This does nothing, since saving into InfluxFB
        # is done in management command save2influxdb
        return True

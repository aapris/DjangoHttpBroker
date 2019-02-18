from celery import shared_task
from .utils import get_datalogger
from broker.endpoint import ForwardProvider


@shared_task
def process_data(devid, data):
    datalogger, created = get_datalogger(devid)
    forwards = datalogger.forwards.all()
    plugins = ForwardProvider.get_plugins({})
    # TODO: this should also search Forwards from
    # - Organisation where this Datalogger belongs to
    # - Group
    for f in forwards:  # Loop all forwards defined to this Datalogger
        for plugin in plugins:  # Find correct plugin
            handler_name = f'{plugin.app}.{plugin.name}'
            print(handler_name)
            if f.handler == handler_name:
                success = plugin.forward_data(data)
    print(data)

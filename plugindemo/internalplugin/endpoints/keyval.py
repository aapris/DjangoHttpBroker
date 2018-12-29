from django.http.response import HttpResponse
from django.utils import timezone

from businesslogic.endpoint import EndpointProvider
from urllib import parse


class KeyValEndpoint(EndpointProvider):
    description = 'Handle data in key=val,key2=val2 format'

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.name = 'KeyVal'  # You may override automatic values here

    def handle_request(self, request):
        # Handle request here and pass data forward and return response as quickly as possible
        response = parse_data(request)
        return response


def parse_data(request):
    """
    Data is in the query string and looks like this:
    dev_id=3AFF42&temp=22.1&humidity=42&pressure=1013.4
    """
    data = dict(parse.parse_qsl(request.META['QUERY_STRING']))
    dev_id = data.pop('dev_id', '')
    ts = timezone.now()
    try:
        values = {key: float(value) for (key, value) in data.items()}
    except ValueError as err:
        response = HttpResponse(f'ValueError: {err}', status=400, content_type='text/plain')
        return response
    value_count = len(values.keys())
    response = HttpResponse(f'Unhandled error, sorry', status=500, content_type='text/plain')
    if dev_id == '':
        response = HttpResponse(f'ERROR: missing parameter "dev_id"', status=400, content_type='text/plain')
    elif value_count == 0:
        response = HttpResponse(f'ERROR: no data in query string', status=400, content_type='text/plain')
    else:
        values['time'] = ts
        # Put data to a queue here (e.g. with task.delay()) for later processing and return response
        response = HttpResponse(f'OK, saved {value_count} data items', content_type='text/plain')
    return response

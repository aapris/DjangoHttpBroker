import datetime
import re

from django.http.response import HttpResponse

from broker.providers.endpoint import EndpointProvider
from broker.utils import (
    serialize_django_request, data_pack,
    save_httprequest_to_file)


class DefaultEndpoint(EndpointProvider):
    description = 'Receive any HTTP request for debugging purposes'

    def handle_request(self, request):
        serialised_request = serialize_django_request(request)
        # Because this can be any kind of data, we create devid from string "unknown" and PATH_INFO part of URL
        devid = 'unknown-{}'.format(serialised_request['request.META']['PATH_INFO'])
        devid = re.sub('[^a-zA-Z0-9-_]', '', devid)
        serialised_request['devid'] = devid
        routing_key = f'broker.default.{devid}'
        serialised_request['time'] = datetime.datetime.utcnow().isoformat() + 'Z'
        message = data_pack(serialised_request)
        save_httprequest_to_file(routing_key, message)
        return HttpResponse('OK', content_type='text/plain')

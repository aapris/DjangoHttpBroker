import json
import msgpack
from io import BytesIO
from django.http.response import HttpResponse
from broker.endpoint import EndpointProvider
from broker.utils import serialize_django_request, data_pack, data_unpack

META_STARTSWITH = ('SERVER', 'REMOTE')
META_EXACT = ('QUERY_STRING', 'REQUEST_METHOD', 'SCRIPT_NAME', 'PATH_INFO')


class DumpRequestEndpoint(EndpointProvider):
    description = 'Endpoint, which serialises HTTP request headers and body'

    def handle_request(self, request):
        serialised_request = serialize_django_request(request)
        # Testing packer and unpacker
        packed_request = data_pack(serialised_request)
        unpacked_request = data_unpack(packed_request)
        assert serialised_request == unpacked_request

        # Construct response json (with limited request body)
        rb = serialised_request['request.body']
        rb = rb.decode('utf8', "backslashreplace")
        body_max_len = 100 * 1  # bytes
        over_len = -(body_max_len - len(rb))  # how many bytes body was too long, if positive
        if over_len > 0:
            rb = f'{rb[:body_max_len]} [...{over_len} bytes stripped...]'
        serialised_request['request.body'] = rb
        json_response = json.dumps(serialised_request)
        return HttpResponse(json_response, content_type='application/json')

import json
import msgpack
from io import BytesIO
from django.http.response import HttpResponse
from broker.endpoint import EndpointProvider

META_STARTSWITH = ('SERVER', 'REMOTE')
META_EXACT = ('QUERY_STRING', 'REQUEST_METHOD', 'SCRIPT_NAME', 'PATH_INFO')


class DumpRequestEndpoint(EndpointProvider):
    description = 'Endpoint, which serialises HTTP request headers and body'

    def handle_request(self, request):
        request_body = request.body
        request_headers = dict(request.headers)
        request_meta = {}
        mkeys = list(request.META.keys())
        mkeys.sort()
        for k in mkeys:
            if k.startswith(META_STARTSWITH) or k in META_EXACT:
                request_meta[k] = request.META[k]
        # Write headers dict and body bytes to msgpack buffer
        buf = BytesIO()
        buf.write(msgpack.packb(request_headers, use_bin_type=True))
        buf.write(msgpack.packb(request_meta, use_bin_type=True))
        buf.write(msgpack.packb(request_body, use_bin_type=True))
        buf.seek(0)  # Now buf could be sent to a task queue

        # Testing unpacker
        # unpacker = msgpack.Unpacker(buf, raw=False)
        # for unpacked in unpacker:
        #     pass
        #     print(type(unpacked), unpacked)

        # Construct response json (with limited request body)
        request_body = request_body.decode('utf8', "backslashreplace")
        body_max_len = 100 * 1  # bytes
        over_len = -(body_max_len - len(request_body))  # how many bytes body was too long, if positive
        if over_len > 0:
            request_body = f'{request_body[:body_max_len]} [...{over_len} bytes stripped...]'
        serialised_request = {
            'request.headers': request_headers,
            'request.META': request_meta,
            'request.body': request_body  # printable version of possibly binary data
        }
        json_response = json.dumps(serialised_request)
        return HttpResponse(json_response, content_type='application/json')

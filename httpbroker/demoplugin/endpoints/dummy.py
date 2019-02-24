from django.http.response import HttpResponse
from broker.providers.endpoint import EndpointProvider


class DummyEndpoint(EndpointProvider):
    description = 'Dummy endpoint, which does nothing but just returns OK'

    def handle_request(self, request):
        # For some reason request.body must be accessed, otherwise there will occur mysterious
        # second request with post payload, at least in development server
        _ = request.body
        return HttpResponse('OK', content_type='text/plain')

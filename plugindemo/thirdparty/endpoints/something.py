from django.http.response import HttpResponse
from businesslogic.endpoint import EndpointProvider


class SomePlugin(EndpointProvider):
    description = 'A plugin implemented by someone'

    def handle_request(self, request):
        # Handle request here and pass data forward and return response as quickly as possible
        return HttpResponse(f'$yes we can!$ {self.name}', content_type='text/plain')

from django.http.response import HttpResponse
from businesslogic.endpoint import EndpointProvider


class ColumnDataEndpoint(EndpointProvider):
    description = 'Handle data in header row + data rows format'

    def handle_request(self, request):
        # Handle request here and pass data forward and return response as quickly as possible
        return HttpResponse(f'$OK$ {self.name}', content_type='text/plain')

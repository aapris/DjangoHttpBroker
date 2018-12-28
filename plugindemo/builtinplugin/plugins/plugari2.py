from django.http.response import HttpResponse
from businesslogic.plugin import EndpointProvider


class Plugari2(EndpointProvider):
    title = 'Plugari2'
    description = 'Builtin app endpoint 2 handler'

    def handle_request(self, request):
        return HttpResponse('$Jee!', content_type='text/plain')

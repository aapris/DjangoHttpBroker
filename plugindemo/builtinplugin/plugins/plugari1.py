from django.http.response import HttpResponse
from businesslogic.plugin import EndpointProvider


class Plugari1(EndpointProvider):
    title = 'Plugari1'
    description = 'Builtin app endpoint handler'

    def handle_request(self, request):
        return HttpResponse('$Jee!', content_type='text/plain')

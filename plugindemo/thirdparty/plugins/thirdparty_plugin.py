from django.http.response import HttpResponse
from businesslogic.plugin import EndpointProvider


class Plugari1(EndpointProvider):
    title = 'ThirdParty'
    description = 'A plugin implemented by someone'

    def handle_request(self, request):
        return HttpResponse('$Jee!', content_type='text/plain')

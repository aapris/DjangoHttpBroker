from django.http.response import HttpResponse
from businesslogic.plugin import EndpointProvider


# This won't get initialised

class BuiltinApp1(EndpointProvider):
    title = 'BuiltinApp1'
    description = 'Builtin app endpoint handler'

    def handle_request(self, request):
        return HttpResponse('OK', content_type='text/plain')

# class BuiltinEndpoint2(EndpointProvider):
#     title = 'BuiltinEndpoint2'
#     description = '2nd endpoint handler'
#
#     def handle_request(self, request):
#         return HttpResponse('$OK$', content_type='text/plain')

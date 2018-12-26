from django.http.response import HttpResponse
from businesslogic.plugin import EndpointProvider

# This won't get initialised

# class BuiltinEndpoint1(EndpointProvider):
#     title = 'BuiltinEndpoint1'
#     description = '1st endpoint handler'
#
#     def handle_request(self, request):
#         return HttpResponse('OK', content_type='text/plain')
#
#
# class BuiltinEndpoint2(EndpointProvider):
#     title = 'BuiltinEndpoint2'
#     description = '2nd endpoint handler'
#
#     def handle_request(self, request):
#         return HttpResponse('$OK$', content_type='text/plain')

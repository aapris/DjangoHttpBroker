from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Endpoint
from .plugin import EndpointProvider


def catchall(request, path):
    endpoint = get_object_or_404(Endpoint, path=path)
    actions = EndpointProvider.get_plugins(request)
    print(actions)
    response = HttpResponse('Handler not found', content_type='text/plain', status=500)
    for a in actions:
        if endpoint.handler == a.title:
            response = a.handle_request(request)
            break
    return response

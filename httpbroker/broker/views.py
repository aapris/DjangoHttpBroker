from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Endpoint
from .endpoint import EndpointProvider


@csrf_exempt
def catchall(request, path):
    """
    Find a right handler for requested path.
    """
    endpoint = get_object_or_404(Endpoint, path=path)
    plugins = EndpointProvider.get_plugins(request)
    response = HttpResponse('Handler not found', content_type='text/plain', status=500)
    for plugin in plugins:
        handler_name = f'{plugin.app}.{plugin.name}'
        if endpoint.handler == handler_name:
            response = plugin.handle_request(request)
            break
    return response

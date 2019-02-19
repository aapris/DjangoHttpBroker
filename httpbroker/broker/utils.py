"""
Sometimes you need to pass forward HttpRequest, which is not directly serializable.
serialize_django_request() takes Django HttpRequest as an argument, extracts 
HttpRequest.headers (available since Django 2.2), HttpRequest.body and most interesting
values out from HttpRequest.META and returns them in a dict which is json, msgpack etc.
serializable.
"""

import msgpack

META_STARTSWITH = ('SERVER', 'REMOTE')  # REMOTE_ADDR etc.
META_EXACT = ('QUERY_STRING', 'REQUEST_METHOD', 'SCRIPT_NAME', 'PATH_INFO')


def serialize_django_request(request):
    """
    Extract all useful values from HttpRequest and return them as a dict.
    :param HttpRequest request:
    :return: HttpRequest headers, META and body in a dict.
    """
    request_meta = {}
    mkeys = list(request.META.keys())
    mkeys.sort()
    for k in mkeys:
        if k.startswith(META_STARTSWITH) or k in META_EXACT:
            request_meta[k] = request.META[k]
    request_meta['path'] = request.META['SCRIPT_NAME'] + request.META['PATH_INFO']

    return {
        'request.headers': dict(request.headers),
        'request.META': request_meta,
        'request.body': request.body,
    }


def data_pack(message):
    """
    Pack message using msgpack.packb() and known arguments.

    :param dict message:
    :return: Packed message
    """
    return msgpack.packb(message, use_bin_type=True, strict_types=True)


def data_unpack(message):
    """
    Unpack message using msgpack.unpackb() and known arguments.

    :param bytes message:
    :return: Message in dict
    """
    return msgpack.unpackb(message, use_list=True, raw=False, strict_map_key=True)

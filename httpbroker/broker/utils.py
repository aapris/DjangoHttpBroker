"""
Sometimes you need to pass forward HttpRequest, which is not directly serializable.
serialize_django_request() takes Django HttpRequest as an argument, extracts 
HttpRequest.headers (available since Django 2.2), HttpRequest.body and most interesting
values out from HttpRequest.META and returns them in a dict which is json, msgpack etc.
serializable.
"""

import base64
import msgpack
import json
import datetime
import pytz
import pika
import pika.exceptions
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone

from broker.providers.decoder import DecoderProvider

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
        'request.GET': dict(request.GET),
        'request.POST': dict(request.POST),
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


def send_message(exchange, key, message):
    if settings.RABBITMQ.get('USER') is not None and settings.RABBITMQ.get('PASSWORD') is not None:
        credentials = pika.PlainCredentials(settings.RABBITMQ['USER'], settings.RABBITMQ['PASSWORD'])
        conn_params = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    else:
        conn_params = pika.ConnectionParameters('localhost', 5672, '/')
    try:
        connection = pika.BlockingConnection(conn_params)
    except pika.exceptions.ConnectionClosed as err:
        print(f'Connection failed {err}')
        # Log error, notify admins, fallback to file storage etc. here
        raise

    channel = connection.channel()
    channel.basic_publish(exchange=exchange,
                          routing_key=key,
                          body=message,
                          properties=pika.BasicProperties(content_type='application/octet-stream',
                                                          delivery_mode=2))
    channel.close()
    connection.close()


def basicauth(request):
    """Check for valid basic auth header."""
    uname, passwd, user = None, None, None
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                a = auth[1].encode('utf8')
                s = base64.b64decode(a)
                uname, passwd = s.decode('utf8').split(':')
                user = authenticate(username=uname, password=passwd)
    return uname, passwd, user


def decode_json_body(body):
    body_str = body.decode('utf8', "backslashreplace")
    try:
        data = json.loads(body_str)
        return True, data
    except json.decoder.JSONDecodeError as err:
        return False, err


def get_datalogger(devid, name='', update_activity=False):
    # FIXME: Shit, this import can't be in the beginning of the file or we'll get:
    # "django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet."
    # It can be imported if you run django.setup() before import, but it messes up loading
    # import django
    # django.setup()
    # from broker.models import Datalogger
    from .models import Datalogger

    datalogger, created = Datalogger.objects.get_or_create(devid=devid)
    changed = False
    if created:
        datalogger.name = name
        changed = True
    if update_activity:
        datalogger.activity_at = timezone.now()
        changed = True
    if changed:
        datalogger.save()
    return datalogger, created


def create_routing_key(module, devid):
    pre = settings.RABBITMQ['ROUTING_KEY_PREFIX']
    key = f'{pre}.{module}.{devid}'
    return key


# Data format and validation tools

def decode_payload(datalogger, payload, port):
    """
    Use `datalogger`'s correct decoder plugin to decode `payload`
    :param datalogger:
    :param payload:
    :param port:
    :return:
    """
    plugins = DecoderProvider.get_plugins({})
    decoded_payload = {}
    for plugin in plugins:
        decoder_name = f'{plugin.app}.{plugin.name}'
        print(datalogger.decoder, decoder_name)
        if datalogger.decoder == decoder_name:
            decoded_payload = plugin.decode_payload(payload, port)
            break
    return decoded_payload


def create_dataline(timestamp: datetime.datetime, data: dict, extra=None):
    """
    Create one dataline for "parsed data" from timestamp and data
    :param datetime timestamp: timezone aware datetime object
    :param dict data: key-value pairs
    :param dict extra:
    :return: dict dataline
    """
    #
    if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
        raise ValueError('timestamp must be timezone aware')
    timestamp = timestamp.astimezone(pytz.UTC)
    dataline = {
        'time': timestamp.isoformat(),
        'data': data
    }
    if extra is not None:
        dataline.update(extra)
    return dataline


def create_parsed_data_message(devid, datalines, extra=None):
    message = {
        'devid': devid,
        'datalines': datalines,
    }
    if extra is not None:
        message.update(extra)
    return message


def validate_parsed_data_message(message, validate_data=False):
    """
    Check that message has valid parsed data structure
    :param dict message: data in parsed data format
    :param bool validate_data: check data values if True
    :return: bool valid or not
    """
    if 'devid' not in message:
        return False
    if 'datalines' not in message:
        return False
    datalines = message['datalines']
    if isinstance(datalines, list) is False:
        return False
    for line in datalines:
        if 'time' not in line or 'data' not in line:
            return False
        if validate_data:
            # TODO: implement these
            # parse time
            # parse data values (are floats)
            pass
    return True

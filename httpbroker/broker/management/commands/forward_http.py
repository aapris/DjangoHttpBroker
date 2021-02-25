import json
import logging

import requests
from django.conf import settings

from broker.management.commands import RabbitCommand
from broker.utils import data_unpack, get_datalogger

NAME = "forward_http"

logger = logging.getLogger(NAME)


def consumer_callback(channel, method, properties, body, options=None):
    """
    Forward HTTP request to another URI.
    """
    parsed_data = data_unpack(body)
    devid = parsed_data["devid"]
    datalogger, created = get_datalogger(devid=devid, update_activity=False)
    config = {}
    if datalogger.application:
        config.update(json.loads(datalogger.application.config))
    # Add to application's config a key like:
    # "forward_http": "http://example.com/dump_request",
    forward_url = config.get("forward_http")
    if forward_url:
        request_method = parsed_data["request.META"]["REQUEST_METHOD"]
        logger.info(f"Forwarding {request_method} {forward_url}\n")
        headers = {}
        for h in ["Content-Type", "User-Agent", "Accept"]:
            headers[h] = parsed_data["request.headers"].get(h)
        request_body = parsed_data["request.body"]
        # print(f"{request_method} {forward_url}\n")
        # for k, v in headers.items():
        #     print(f"{k}: {v}")
        # print()
        # print(request_body)
        res = requests.request(request_method, forward_url, headers=headers, data=request_body)
        if str(res.status_code).startswith("2"):
            logger.info(f"{res.status_code} {res.text}")
        else:
            logger.warning(f"{res.status_code} {res.text} from {forward_url}")
    else:
        logger.debug(f"No forward for device: {devid}")
    channel.basic_ack(method.delivery_tag)


class Command(RabbitCommand):
    help = "Read RabbitMQ queue and save all data into InfluxDB"

    def add_arguments(self, parser):
        parser.add_argument(
            "--prefix", type=str, help="queue and routing_key prefix, overrides settings.ROUTING_KEY_PREFIX"
        )
        super().add_arguments(parser)

    def handle(self, *args, **options):
        logging.basicConfig(level=getattr(logging, options["log"]))
        logger.info(f"Start handling {__name__}")
        name = NAME
        # FIXME: constructing options should be in a function in broker.utils
        if options["prefix"] is None:
            prefix = settings.RABBITMQ["ROUTING_KEY_PREFIX"]
        else:
            prefix = options["prefix"]
        options["exchange"] = settings.RAW_HTTP_EXCHANGE
        # options['routing_key'] = f'{prefix}.{name}.#'
        options["routing_key"] = f"{prefix}.#"
        options["queue"] = f"{prefix}_{name}_queue"
        options["consumer_callback"] = consumer_callback
        super().handle(*args, **options)

import pika

# Exchange names. Note: these are in settings.py too!
RAW_HTTP_EXCHANGE = 'incoming_raw_http'
PARSED_DATA_EXCHANGE = 'outgoing_parsed_data'
PARSED_DATA_HEADERS_EXCHANGE = 'outgoing_parsed_data_headers'

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', 5672, '/',
                              # pika.credentials.PlainCredentials('user', 'password')
                              ))

channel = connection.channel()

channel.exchange_declare(
    exchange=RAW_HTTP_EXCHANGE,
    exchange_type='topic',
    durable=True,
    auto_delete=False,
)

channel.exchange_declare(
    exchange=PARSED_DATA_EXCHANGE,
    exchange_type='topic',
    durable=True,
    auto_delete=False,
)

channel.exchange_declare(
    exchange=PARSED_DATA_HEADERS_EXCHANGE,
    exchange_type='headers',
    durable=True,
    auto_delete=False,
)

channel.close()
connection.close()

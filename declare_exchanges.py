import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', 5672, '/',
                              # pika.credentials.PlainCredentials('user', 'password')
                              ))

channel = connection.channel()
channel.exchange_declare(
    exchange='incoming_raw_http',
    exchange_type='topic',
    durable=True,
    auto_delete=False,
)

channel.close()
connection.close()

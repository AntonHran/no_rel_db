import os
import sys

import pika

from model import User
from producer import user, password, host, queue_name


def main():
    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                                   port=5672,
                                                                   credentials=credentials,
                                                                   virtual_host=user))
    chanel = connection.channel()

    chanel.queue_declare(queue=queue_name, durable=True)

    # consumer = "HAE"

    def callback(ch, method, properties, body):
        pk = body.decode()
        user_ = User.objects(id=pk, email_sent=False)
        if user_:
            user_.update(set__email_sent=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    chanel.basic_qos(prefetch_count=1)
    chanel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(" [x] Waiting for messages. To exit press CTRL+C")
    chanel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

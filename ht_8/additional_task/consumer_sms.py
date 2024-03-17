import os
import sys

import pika

from model import User
from producer import user, password, host, sms_queue


def main():
    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                                   port=5672,
                                                                   credentials=credentials,
                                                                   virtual_host=user))
    chanel = connection.channel()

    chanel.queue_declare(queue=sms_queue, durable=True)

    consumer = "sms_consumer"

    def callback(ch, method, properties, body):
        pk = body.decode()
        user_ = User.objects(id=pk, message_sent=False).first()
        if user_:
            user_.update(set__message_sent=True)
            print(f" [x] {consumer} has sent message to {user_.fullname} ({pk}) through phone: {user_.phone}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    chanel.basic_qos(prefetch_count=1)
    chanel.basic_consume(queue=sms_queue, on_message_callback=callback)

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

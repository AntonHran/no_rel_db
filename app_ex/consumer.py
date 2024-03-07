import os
import sys

import pika

from app_ex.models import Task
from app_ex.app_ import user, password, host, queue_name


def main():
    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                                   port=5672,
                                                                   credentials=credentials,
                                                                   virtual_host=user))
    chanel = connection.channel()

    chanel.queue_declare(queue=queue_name, durable=True)

    consumer = "HAE"

    def callback(ch, method, properties, body):
        pk = body.decode()
        task = Task.objects(id=pk, completed=False)
        if task:
            task.update(set__completed=True, set__consumer=consumer)
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

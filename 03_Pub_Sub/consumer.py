import os
import sys
import json

import pika


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
    chanel = connection.channel()

    q = chanel.queue_declare(queue="", exclusive=True)
    name_q = q.method.queue
    chanel.queue_bind(exchange="Events Message", queue=name_q)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        print(f" [x] Received: {message}")

    # chanel.basic_qos(prefetch_count=1)
    chanel.basic_consume(queue=name_q, on_message_callback=callback)

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

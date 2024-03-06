import os
import sys
import json
import time

import pika


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
    chanel = connection.channel()

    chanel.queue_declare(queue="queue_name")

    def callback(ch, method, body):
        message = json.load(body.decode())
        print(f" [x] Received: {message}")
        time.sleep(0.5)
        print(f" [x] Completed task: {method.delivery_tag}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    chanel.basic_qos(prefetch_count=1)
    chanel.basic_consume(queue="queue_name", on_message_callback=callback)

    print(" [x] Waiting for messages. To exit press CTRL+C")
    chanel.stop_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

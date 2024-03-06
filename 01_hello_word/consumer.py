import os
import sys

import pika


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
    chanel = connection.channel()

    chanel.queue_declare(queue="hello", durable=True)

    def callback(ch, method, body):
        print(f" [x] Received: {body.decode()}")

    chanel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

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

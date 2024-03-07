import json
from datetime import datetime

import pika


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
chanel = connection.channel()

chanel.exchange_declare(exchange="Events Message", exchange_type="fanout")


def create_event():
    message = {
        "event": "Test event",
        "message": "Test message",
        "payload": f"Date: {datetime.now().isoformat()}"
    }
    chanel.basic_publish(exchange="Events Message", routing_key="", body=json.dumps(message).encode())
    connection.close()


if __name__ == '__main__':
    create_event()

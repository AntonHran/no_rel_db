import json
from datetime import datetime

import pika


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials))
chanel = connection.channel()

chanel.exchange_declare(exchange="Exchange_Name", exchange_type="direct")
chanel.queue_declare(queue="queue_name")
chanel.queue_bind(exchange="Exchange_Name", queue="queue_name")


def create_task(nums: int):
    for i in range(nums):
        message = {
            "id": i,
            "payload": f"Date: {datetime.now().isoformat()}"
        }
        chanel.basic_publish(exchange="Exchange_Name", routing_key="queue_name", body=json.dumps(message).encode())
    connection.close()


if __name__ == '__main__':
    create_task(100)

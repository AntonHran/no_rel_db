import json
from datetime import datetime
import configparser
import pathlib

import pika


file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

user = config.get("CloudRMQ", "USER")
password = config.get("CloudRMQ", "PASSWORD")
host = config.get("CloudRMQ", "DB_NAME")

credentials = pika.PlainCredentials(user, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                               port=5672,
                                                               credentials=credentials,
                                                               virtual_host=user))
chanel = connection.channel()

chanel.exchange_declare(exchange="Exchange_Service", exchange_type="direct")
chanel.queue_declare(queue="m8", durable=True)
chanel.queue_bind(exchange="Exchange_Service", queue="m8")


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

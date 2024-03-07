import configparser
import pathlib

import pika

from app_ex.models import Task


file_config = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

user = config.get("CloudRMQ", "USER")
password = config.get("CloudRMQ", "PASSWORD")
host = config.get("CloudRMQ", "HOST")

exchange_name = "Exchange_Service"
queue_name = "m8"

credentials = pika.PlainCredentials(user, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                               port=5672,
                                                               credentials=credentials,
                                                               virtual_host=user))
chanel = connection.channel()

chanel.exchange_declare(exchange=exchange_name, exchange_type="direct")
chanel.queue_declare(queue=queue_name, durable=True)
chanel.queue_bind(exchange=exchange_name, queue=queue_name)


def create_task(nums: int):
    for i in range(nums):
        task = Task(consumer="No name").save()
        chanel.basic_publish(exchange=exchange_name, routing_key=queue_name,
                             body=str(task.id).encode(),
                             properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    connection.close()


if __name__ == '__main__':
    create_task(1)

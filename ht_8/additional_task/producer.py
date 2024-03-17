import configparser
import pathlib
from random import randint

import pika
from faker import Faker

from model import User


file_config = pathlib.Path(__file__).parent.parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

user = config.get("CloudRMQ", "USER")
password = config.get("CloudRMQ", "PASSWORD")
host = config.get("CloudRMQ", "HOST")

exchange_name = "Email_Service"
queue_name = "emails_to_send"

credentials = pika.PlainCredentials(user, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                               port=5672,
                                                               credentials=credentials,
                                                               virtual_host=user))
chanel = connection.channel()

chanel.exchange_declare(exchange=exchange_name, exchange_type="direct")
chanel.queue_declare(queue=queue_name, durable=True)
chanel.queue_bind(exchange=exchange_name, queue=queue_name)

fake = Faker()


def create_task(nums: int):
    for i in range(nums):
        user_ = User(fullname=fake.name(),
                     phone_number=fake.phone_number(),
                     email=fake.email(),
                     position=fake.job()).save()
        chanel.basic_publish(exchange=exchange_name, routing_key=queue_name,
                             body=str(user_.id).encode(),
                             properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    connection.close()


if __name__ == '__main__':
    create_task(randint(1, 100))

import configparser
import pathlib
from random import randint, choice

import pika
from faker import Faker

from model import User


file_config = pathlib.Path(__file__).parent.parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

user = config.get("CloudRMQ", "USER")
password = config.get("CloudRMQ", "PASSWORD")
host = config.get("CloudRMQ", "HOST")

exchange_name = "Message_Service"
emails_queue = "emails_to_send"
sms_queue = "sms_to_send"

credentials = pika.PlainCredentials(user, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,
                                                               port=5672,
                                                               credentials=credentials,
                                                               virtual_host=user))
chanel = connection.channel()

chanel.exchange_declare(exchange=exchange_name, exchange_type="direct")
chanel.queue_declare(queue=emails_queue, durable=True)
chanel.queue_bind(exchange=exchange_name, queue=emails_queue)

chanel.queue_declare(queue=sms_queue, durable=True)
chanel.queue_bind(exchange=exchange_name, queue=sms_queue)

fake = Faker()
connecting_options = ["email", "phone"]


def create_user():
    user_ = User(fullname=fake.name(),
                 phone=fake.phone_number(),
                 email=fake.email(),
                 preferable_connection=choice(connecting_options),
                 position=fake.job()).save()
    return user_


def create_task(nums: int):
    for i in range(nums):
        user_ = create_user()
        if user_.preferable_connection == "email":
            chanel.basic_publish(exchange=exchange_name, routing_key=emails_queue,
                                 body=str(user_.id).encode(),
                                 properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        else:
            chanel.basic_publish(exchange=exchange_name, routing_key=sms_queue,
                                 body=str(user_.id).encode(),
                                 properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    connection.close()


if __name__ == '__main__':
    create_task(randint(1, 50))

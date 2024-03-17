from mongoengine import connect, Document, StringField, BooleanField

from app import uri


connect(db="quotes", host=uri)


class User(Document):
    fullname = StringField(required=True, unique=True)
    phone = StringField(max_length=30)
    email = StringField(max_length=100)
    preferable_connection = StringField()
    message_sent = BooleanField(default=False)
    position = StringField()
    meta = {"collection": "users"}

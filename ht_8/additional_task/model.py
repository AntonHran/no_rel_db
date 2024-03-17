from mongoengine import connect, Document, StringField, BooleanField

from app import uri


connect(db="quotes", host=uri)


class User(Document):
    fullname = StringField(required=True, unique=True)
    phone_number = StringField(max_length=30)
    email = StringField(max_length=100)
    email_sent = BooleanField(default=False)
    position = StringField()
    meta = {"collection": "users"}

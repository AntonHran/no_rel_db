from mongoengine import connect, Document, StringField, BooleanField

from app import uri


connect(db="test", host=uri)


class Task(Document):
    completed = BooleanField(default=False)
    consumer = StringField(max_length=150)

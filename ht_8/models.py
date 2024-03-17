from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE
from mongoengine.errors import DoesNotExist

from app import uri


connect(db="quotes", host=uri)


class Author(Document):
    full_name = StringField(required=True, unique=True)
    born_date = StringField(max_length=30)
    born_location = StringField(max_length=100)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=40))
    quote = StringField(required=True, unique=True)
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        try:
            data["author"] = self.author.full_name
            return json_util.dumps(data, ensure_ascii=False)
        except DoesNotExist:
            print(f"There is not such author with id: {self.author}")

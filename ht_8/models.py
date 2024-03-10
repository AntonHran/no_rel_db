from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE


connect(db="quotes", host="mongodb://localhost:27017")


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=30)
    born_location = StringField(max_length=100)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=20))
    quote = StringField()
    meta = {"collection": "quotes"}

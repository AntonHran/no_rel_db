import argparse

from bson.objectid import ObjectId
from mongoengine import connect, Document, StringField, IntField, ListField


uri = "mongodb+srv://tgranowsky:1k5DbllkCKU7UVYj@cluster0.xzz8ywk.mongodb.net/?retryWrites=true&w=majority"

connect(db="test", host=uri)

parser = argparse.ArgumentParser(description="Server Cats Enterprise")
parser.add_argument("--action", help="create, read, update, delete")
parser.add_argument("--id")
parser.add_argument("--name")
parser.add_argument("--age")
parser.add_argument("--features", nargs="+")

args = vars(parser.parse_args())

action = args.get("action")
pk = args.get("id")
name = args.get("name")
age = args.get("age")
features = args.get("features")


class Cat(Document):
    name = StringField(max_length=120, required=True)
    age = IntField(min_value=1, max_value=30)
    features = ListField(StringField(max_length=150))
    meta = {"collection": "cats"}


def find():
    return db.cats.find()


def create(name_: str, age_: int, features_: list):
    new_record = db.cats.insert_one(
        {"name": name_,
         "age": age_,
         "features": features_, }
    )
    return new_record


def update(pk_: str, name_: str, age_: int, features_: list):
    update_record = db.cats.update_one({"_id": ObjectId(pk_)}, {
        "$set": {

            "name": name_,
            "age": age_,
            "features": features_,
        }})
    return update_record


def delete(pk_: str):
    return db.cats.delete_one({"_id": ObjectId(pk_)})


def main():
    match action:
        case "create":
            res = create(name, age, features)
            print(res)
        case "read":
            res = find()
            print([el for el in res])
        case "update":
            res = update(pk, name, age, features)
            print(res)
        case "delete":
            res = delete(pk)
            print(res)
        case _:
            print("Unknown command")


if __name__ == '__main__':
    main()

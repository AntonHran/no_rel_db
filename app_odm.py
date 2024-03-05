import argparse

from mongoengine import connect, Document, StringField, IntField, ListField, DoesNotExist

from app import uri


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
    return Cat.objects.all()


def create(name_: str, age_: int, features_: list):
    new_record = Cat(name=name_, age=age_, features=features_)
    new_record.save()
    return new_record


def update(pk_: str, name_: str, age_: int, features_: list):
    update_record = Cat.objects(id=pk_).first()  # return cat of None
    if update_record:
        update_record.update(name=name_, age=age_, features=features_)
        update_record.reload()
    return update_record


def delete(pk_: str):
    try:
        cat_to_del = Cat.objects.get(id=pk_)  # if cat does not exist it returns error DoesNotExist
        cat_to_del.delete()
        return cat_to_del
    except DoesNotExist as err:
        print(err)
        return None


def main():
    match action:
        case "create":
            res = create(name, age, features)
            print(res.to_mongo().to_dict())
        case "read":
            res = find()
            print([el.to_mongo().to_dict() for el in res])
        case "update":
            res = update(pk, name, age, features)
            if res:
                print(res.to_mongo().to_dict())
        case "delete":
            res = delete(pk)
            if res:
                print(res.to_mongo().to_dict())
        case _:
            print("Unknown command")


if __name__ == '__main__':
    main()

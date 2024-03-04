import argparse

from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = ""

client = MongoClient(uri, server_api=ServerApi("1"))
db = client.test

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


def find():
    ...


def create(name: str, age: int, features: list | str):
    ...


def update(pk: int, name: str, age: int, features: list | str):
    ...


def delete(pk: int):
    ...


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


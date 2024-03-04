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



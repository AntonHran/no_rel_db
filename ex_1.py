from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app import uri


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.test

# Send a ping to confirm a successful connection
try:
    result_many = db.cats.insert_many(
        [
            {
                "name": "Lama",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Liza",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
            {
                "name": 'Boris',
                "age": 12,
                "features": ['ходить в лоток', 'не дає себе гладити', 'сірий'],
            },
            {
                "name": 'Murzik',
                "age": 1,
                "features": ['ходить в лоток', 'дає себе гладити', 'чорний'],
            }
        ]
    )
    print(result_many.inserted_ids)
except Exception as e:
    print(e)

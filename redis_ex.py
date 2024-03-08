import pickle

import redis


client = redis.Redis(host="localhost", port=6379, password=None)

if __name__ == '__main__':
    client.set("username1", "Artem")
    client.set("username2", "Natalia")
    client.expire("username1", 600)

    client.set("count", 100)
    res = client.get("count")
    print(int(res))

    client.set("test_list", pickle.dumps([2, 3, 4]))
    res = client.get("test_list")
    print(pickle.loads(res))
    
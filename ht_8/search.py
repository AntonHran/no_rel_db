from mongoengine.errors import MongoEngineException, DoesNotExist
from redis import StrictRedis
from redis_lru import RedisLRU

from models import Author, Quote


client = StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def search_by_author(author: str):
    try:
        author_obj = Author.objects.filter(fullname__iregex=author).first()
        quotes = Quote.objects.filter(author=author_obj.id).all()
        return quotes
    except DoesNotExist:
        print("NWF")
    except AttributeError:
        print("error")


@cache
def search_by_tag(tag: str):
    try:
        quotes = Quote.objects(tags__iregex=tag).all()
        return quotes
    except MongoEngineException:
        print('some error')


def search_by_tags(tags: str):
    tags_ = tags.split(",")
    res = []
    for tag in tags_:
        quotes = search_by_tag(tag)
        if quotes:
            res.append(*quotes)
    # print(res)
    return set(res)


def get_all_quotes():
    quotes = Quote.objects().all()
    print([quote.to_json() for quote in quotes])


def print_result(quotes):
    if quotes:
        [print(quote.to_mongo().to_dict().get("quote")) for quote in quotes]
    else:
        print("Nothing")


def parse_entered_str(search: str):
    try:
        field, value = search.split(":")
        match field:
            case "name":
                return search_by_author(value)
            case "tag":
                return search_by_tag(value)
            case "tags":
                return search_by_tags(value)
            case "quotes":
                return get_all_quotes()
            case _:
                print("Unknown field")
    except ValueError as err:
        print(err)


def main():
    while True:
        search = input("\nTo search enter <field>:<value> ---> ")
        if search == "exit":
            break
        quotes = parse_entered_str(search)
        print_result(quotes)


if __name__ == "__main__":
    main()
    # print_result(search_by_author("Albert Einstein"))

from mongoengine.errors import MongoEngineException, DoesNotExist
from redis import StrictRedis
from redis_lru import RedisLRU

from models import Author, Quote


client = StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def search_by_author(authors: list) -> list:
    res = []
    for author in authors:
        quotes = Quote.objects.filter(author=author.id).all()
        print(quotes)
        res.extend(quotes)
    return res


def get_all_authors(author: str) -> list:
    try:
        authors_objs = Author.objects.filter(full_name__iregex=author).all()
        # print(authors_objs)
        return authors_objs
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
            res.extend(quotes)
    # print(res)
    return set(res)


def get_all_quotes():
    quotes = Quote.objects().all()
    [print(quote.to_json()) for quote in quotes]


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
                authors = get_all_authors(value)
                return search_by_author(authors)
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

import json
import typing

from mongoengine.errors import NotUniqueError

from models import Author, Quote


def seed_authors(el: dict) -> None:
    try:
        author = Author(fullname=el.get("fullname"), born_date=el.get("born_date"),
                        born_location=el.get("born_location"),
                        description=el.get("description"))
        author.save()
    except NotUniqueError:
        print(f"Author already exists: {el.get('fullname')}")


def seed_quotes(el: dict) -> None:
    try:
        # author, *_ = Author.objects(fullname=el.get("author"))
        author = Author.objects.filter(fullname=el.get("author"))
        # print(author.get().id)
        quote = Quote(author=author.get().id,
                      tags=el.get("tags"),
                      quote=el.get("quote"))
        quote.save()
    except NotUniqueError:
        print(f"Quote already exists: {el.get('quote')}")


def write_from_json(filename: str, func: typing.Callable) -> None:
    with open(filename, encoding="utf-8") as fd:
        data: list[dict] = json.load(fd)
        for el in data:
            func(el)


def main():



if __name__ == '__main__':
    write_from_json("authors.json", seed_authors)
    write_from_json("quotes.json", seed_quotes)

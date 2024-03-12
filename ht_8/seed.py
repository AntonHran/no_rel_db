import json

from mongoengine.errors import NotUniqueError

from models import Author, Quote


def seed_authors(filename: str) -> None:
    with open(filename, encoding="utf-8") as fd:
        data: list[dict] = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get("fullname"), born_date=el.get("born_date"),
                                born_location=el.get("born_location"),
                                description=el.get("description"))
                author.save()
            except NotUniqueError:
                print(f"Author already exists: {el.get('fullname')}")


def seed_quotes(filename: str) -> None:
    with open(filename, encoding="utf-8") as fd:
        data: list[dict] = json.load(fd)
        for el in data:
            # author, *_ = Author.objects(fullname=el.get("author"))
            print(Author.objects(fullname=el.get("fullname")))
            # quote = Quote(author=author,
                          # tags=el.get("tags"),
                          # quote=el.get("quote"))
            # quote.save()


if __name__ == '__main__':
    seed_authors("authors.json")
    seed_quotes("quotes.json")

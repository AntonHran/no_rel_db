from models import Author, Quote


def search_by_author(author: str):
    author_obj = Author.objects.filter(fullname=author).first()
    quotes = Quote.objects.filter(author=author_obj.get().id).all()
    return quotes


def search_by_tag(tag: str):
    quotes = Quote.objects(tags=tag).all()
    return quotes


def search_by_tags(tags: str):
    tags_ = tags.split(",")
    res = []
    for tag in tags_:
        quotes = search_by_tag(tag)
        if quotes:
            res.append(quotes)
    print(res)
    return set(*res)


def print_result(quotes):
    if quotes:
        [print(quote.to_mongo().to_dict().get("quote")) for quote in quotes]
    else:
        print("Nothing")


if __name__ == "__main__":
    # search_by_author("Albert Einstein")
    q = search_by_tags("life,live")
    print_result(q)

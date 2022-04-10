# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from books.models import Author,Book,Chapter
from scrapy_djangoitem import DjangoItem


class AuthorItem(DjangoItem):
    django_model = Author

class BookItem(DjangoItem):
    django_model = Book

class ChapterItem(DjangoItem):
    django_model = Chapter
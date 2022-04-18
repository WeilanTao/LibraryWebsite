from termios import TAB0
from django.db import models
import sys

sys.path.append("../Library")
import books


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_first_login = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)


class UserToBookList(models.Model):
    booklist_id = models.BigAutoField(auto_created=True, primary_key=True)
    user_id = models.IntegerField()
    booklist_title = models.CharField(max_length=255)


class BookList(models.Model):
    booklist_id = models.IntegerField()
    book_tag = models.CharField(max_length=255)


class Cart(models.Model):
    c_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    c_books_tag = models.ForeignKey(books.models.Book, on_delete=models.CASCADE)

    c_book_num = models.IntegerField(default=1)
    c_is_buy = models.BooleanField(default=True)

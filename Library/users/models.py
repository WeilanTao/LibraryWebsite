from django.db import models
import sys

sys.path.append("../Library")
import books


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)


class UserToBookList(models.Model):
    data_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    booklist_id = models.IntegerField()
    booklist_title = models.CharField(max_length=255)


class BookList(models.Model):
    booklist_id = models.ForeignKey(UserToBookList, on_delete=models.CASCADE)
    book_id = models.ForeignKey(books.models.Book, on_delete=models.CASCADE)

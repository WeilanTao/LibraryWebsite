from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Author(models.Model):
    author_tag = models.CharField(max_length = 255, primary_key=True)
    author_name = models.CharField(max_length = 255)

class Book(models.Model):
    book_tag = models.CharField(max_length = 255, primary_key=True)
    book_name = models.CharField(max_length = 255)
    author_tag = models.CharField(max_length = 255)
    # # to delete the book when the author is deleted-- cascading
    # author_tag = models.ForeignKey(Author, on_delete=models.CASCADE)

class Chapter(models.Model):
    chapter_index = models.CharField(max_length = 255)
    chapter_name= models.CharField(max_length = 255)
    book_tag = models.CharField(max_length = 255)
    chapter_content= models.TextField(default='SOME STRING')
    # book_tag = models.ForeignKey(Book, on_delete=models.CASCADE )
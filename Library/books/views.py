from django.shortcuts import render
from django.http import HttpResponse
from books.models import Author, Book, Chapter
import sys 
import os

# Create your views here.
def index(request):

    return HttpResponse("this is: ", sys.path.append(os.path.dirname(os.path.abspath('.'))))


def get_authors(request):
    authors = Author.objects.values()

    return HttpResponse(authors)

def get_books(request):
    books = Book.objects.values()

    return HttpResponse(books)       

def get_chapters(request):
    chapters = Chapter.objects.values()

    return HttpResponse(chapters)
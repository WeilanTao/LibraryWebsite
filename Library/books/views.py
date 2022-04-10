from django.shortcuts import render
from django.http import HttpResponse
from books.models import Author, Book, Chapter
import sys 
import os

# Create your views here.
def get_authors(request):
    authors = Author.objects.order_by('author_name')

    data ={
        "authors": authors
    }

    return render(request, 'authorslist.html', context = data)

def get_books(request):
    books = Book.objects.values()

    return HttpResponse(books)       

def get_chapters(request):
    chapters = Chapter.objects.values()

    return HttpResponse(chapters)
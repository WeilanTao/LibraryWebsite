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

def get_books(request, auth_tag):
    books = Book.objects.filter(author_tag = auth_tag)

    data={
        "books":books,
        "auth_tag" : auth_tag
    }

    return render(request, 'booklist.html', context=data)       

def get_chapters(request, auth_tag, book_tag):
    chapters = Chapter.objects.filter(book_tag = book_tag).defer('chapter_content').order_by('chapter_name')

    data = {
        "chapters":chapters
    }

    return render(request, 'chapterlist.html', context=data)

def get_chapter_content(request):
    
    return HttpResponse("Hello")
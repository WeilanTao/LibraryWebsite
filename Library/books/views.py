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
    chapters = Chapter.objects.filter(book_tag = book_tag).defer('chapter_content').order_by('chapter_index')

    data = {
        "chapters":chapters,
        'author':auth_tag
    }

    return render(request, 'chapterlist.html', context=data)

def get_chapter_content(request, auth_tag, book_tag, chapter_id):

    chapter = Chapter.objects.filter(id = chapter_id).first()

    data ={
        "chapter":chapter,
        "author": auth_tag
    }

    return render(request, 'chaptercontent.html', context=data)

def get_next_previous(request, auth_tag, book_tag, chapter_id, next_previous):
    chapters = Chapter.objects.filter(book_tag = book_tag).defer('chapter_content').order_by('chapter_index')

    # print(type(next_previous), type(0))
    if(next_previous == "0"):
        chapters = chapters.reverse()
    
    chapterslist = list(chapters)

    isFound = 0
 

    for chapter in chapterslist:        
        if isFound == 1:
            data = {
                "chapter":chapter,
                "author": auth_tag
            }
            return render(request, 'chaptercontent.html', context=data)
        if str(chapter.id) == chapter_id:
            print("Found")
            isFound = 1

    return HttpResponse("hELLO")



def get_previous_chapter(request, auth_tag, book_tag, chapter_id):
    chapters = list(Chapter.objects.filter(book_tag = book_tag).defer('chapter_content').order_by('chapter_index').reverse())

    isFound = 0
 

    for chapter in chapters:        
        if isFound == 1:
            data = {
                "chapter":chapter,
                "author": auth_tag
            }
            return render(request, 'chaptercontent.html', context=data)
        if str(chapter.id) == chapter_id:
            print("Found")
            isFound = 1

    return HttpResponse("hELLO")    
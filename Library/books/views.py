from django.shortcuts import render
from django.http import HttpResponse
from books.models import Author, Book, Chapter
import sys
import os

# Create your views here.
def get_authors(request):
    authors = Author.objects.order_by("author_name")
    data = {"authors": authors}

    return render(request, "books/authorslist.html", context=data)


def get_books(request, author_tag):
    books = Book.objects.filter(author_tag=author_tag)

    author_name = get_author_name(author_tag)

    data = {"books": books, "author_tag": author_tag, "author_name": author_name}

    return render(request, "books/booklist.html", context=data)


def get_chapters(request, author_tag, book_tag):
    chapters = (
        Chapter.objects.filter(book_tag=book_tag)
        .defer("chapter_content")
        .order_by("chapter_index")
    )

    book_name = get_book_name(book_tag)

    data = {"chapters": chapters, "author_tag": author_tag, "book_name": book_name}

    return render(request, "books/chapterlist.html", context=data)


def get_chapter_content(request, author_tag, book_tag, chapter_id):

    chapter = Chapter.objects.filter(id=chapter_id).first()
    book_name = get_book_name(book_tag)
    data = {"chapter": chapter, "author_tag": author_tag, "book_name": book_name}

    return render(request, "books/chaptercontent.html", context=data)


def get_next_previous(request, author_tag, book_tag, chapter_id, next_previous):
    chapters = (
        Chapter.objects.filter(book_tag=book_tag)
        .defer("chapter_content")
        .order_by("chapter_index")
    )

    # print(type(next_previous), type(0))
    if next_previous == "0":
        chapters = chapters.reverse()

    chapterslist = list(chapters)

    isFound = 0

    book_name = get_book_name(book_tag)

    for chapter in chapterslist:
        if isFound == 1:
            data = {
                "chapter": chapter,
                "author_tag": author_tag,
                "book_name": book_name,
            }
            return render(request, "books/chaptercontent.html", context=data)
        if str(chapter.id) == chapter_id:
            print("Found")
            isFound = 1

    return HttpResponse("hELLO")


def get_author_name(author_tag):
    res_name = Author.objects.filter(author_tag=author_tag).only("author_name").first()
    return res_name.author_name


def get_book_name(book_tag):
    res_name = Book.objects.filter(book_tag=book_tag).only("book_name").first()
    return res_name.book_name

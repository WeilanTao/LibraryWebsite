from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from books.models import Author, Book, Chapter
from django.http import HttpResponseRedirect
import sys
import os
import util

# Create your views here.
def get_authors(request):
    authors = Author.objects.order_by("author_name")

    if authors.exists():
        data = {"authors": authors}
        return render(request, "books/authorslist.html", context=data)

    return util.handler404(request)


def get_books(request, author_tag):

    books = Book.objects.filter(author_tag=author_tag)

    if books.exists():
        author_name = get_author_name(author_tag)
        data = {"books": books, "author_tag": author_tag, "author_name": author_name}

        return render(request, "books/booklist.html", context=data)

    return util.handler404(request)


def get_chapters(request, author_tag, book_tag):
    chapters = (
        Chapter.objects.filter(book_tag=book_tag)
        .defer("chapter_content")
        .order_by("chapter_index")
    )
    if chapters.exists():
        book_name = get_book_name(book_tag)
        data = {"chapters": chapters, "author_tag": author_tag, "book_name": book_name}

        return render(request, "books/chapterlist.html", context=data)

    return util.handler404(request)


def get_chapter_content(request, author_tag, book_tag, chapter_id):

    if not chapter_id.isdigit():
        return util.handler404(request)

    chapter = Chapter.objects.filter(id=chapter_id).first()

    if chapter:
        book_name = get_book_name(book_tag)
        data = {"chapter": chapter, "author_tag": author_tag, "book_name": book_name}

        return render(request, "books/chaptercontent.html", context=data)

    return util.handler404(request)


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
    data = {}
    for chapter in chapterslist:
        if isFound == 1:
            data["chapter"] = chapter
            data["author_tag"] = author_tag
            data["book_name"] = book_name
            return render(request, "books/chaptercontent.html", context=data)
        if str(chapter.id) == chapter_id:
            data["chapter"] = chapter
            data["author_tag"] = author_tag
            data["book_name"] = book_name
            # print("Found")
            isFound = 1

    return render(request, "books/chaptercontent.html", context=data)


def get_author_name(author_tag):
    res_name = Author.objects.filter(author_tag=author_tag).only("author_name").first()
    return res_name.author_name


def get_book_name(book_tag):
    res_name = Book.objects.filter(book_tag=book_tag).only("book_name").first()
    return res_name.book_name


def getBookInfo(request):
    book_tag = request.GET.get("book_tag")
    book = list(Book.objects.filter(book_tag=book_tag).values())
    data = {}
    data["book"] = book
    return JsonResponse(data=data)

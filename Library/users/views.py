import imp
from multiprocessing import context
from re import U
import sys
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from users.models import Users, UserToBookList, BookList
from django.urls import reverse, resolve
from django.contrib.auth.hashers import make_password, check_password
from django.core import serializers


sys.path.append("../Library")
import constant


# Create your views here.
## The BookList System
def createBookList(request):
    user = request.user
    user_id = user.id

    data = {}

    booklist_title = request.GET.get("booklist_title")
    usertobooklist = UserToBookList()
    usertobooklist.user_id = user_id
    usertobooklist.booklist_title = booklist_title

    usertobooklist.save()
    # print(usertobooklist.booklist_id)
    data["status"] = 200
    data["msg"] = "book list created"
    data["booklist_id"] = usertobooklist.booklist_id

    return JsonResponse(data=data)


def getUserBookLists(request):
    user = request.user
    user_id = user.id

    data = {}
    userbooklist = UserToBookList.objects.filter(user_id=user_id).values()
    data["userbooklist"] = list(userbooklist)
    data["status"] = 200
    data["msg"] = "user books get"

    return JsonResponse(data=data)


def addBookToList(request):
    data = {"status": constant.HTTP_OK, "msg": "ok"}
    book_list_id = request.GET.get("book_list_id")
    book_tag = request.GET.get("book_tag")
    booklist = BookList()
    booklist.booklist_id = book_list_id
    booklist.book_tag = book_tag
    booklist.save()
    return JsonResponse(data=data)


def getBookList(request):
    booklist_id = request.GET.get("booklist_id")
    books = list(BookList.objects.filter(booklist_id=booklist_id).values())

    data = {}

    data["books"] = books
    return JsonResponse(data=data)


def deleteBookList(request):
    # return HttpResponse("hellp")
    booklist_id = request.GET.get("booklist_id")
    BookList.objects.filter(booklist_id=booklist_id).delete()
    UserToBookList.objects.filter(booklist_id=booklist_id).delete()

    data = {"status": constant.HTTP_OK, "msg": "ok"}

    return JsonResponse(data=data)


def deleteBookFromList(request):
    book_tag = request.GET.get("book_tag")
    booklist_id = request.GET.get("booklist_id")

    BookList.objects.filter(booklist_id=booklist_id, book_tag=book_tag).delete()

    data = {"status": constant.HTTP_OK, "msg": "ok"}

    return JsonResponse(data=data)


## The login System
def logout(request):
    user_id = request.session.get("user_id")

    if user_id:
        request.session.flush()

    return redirect(reverse("books:get_authors"))


# display the usercenter
def mine(request):
    user = request.user
    user_id = user.id
    data = {}

    user = Users.objects.get(id=user_id)
    userbooklists = UserToBookList.objects.filter(user_id=user_id).values()

    data["username"] = user.name
    data["booklists"] = userbooklists

    return render(request, "users/usercenter.html", context=data)


def login(request):
    if request.method == "GET":
        return render(request, "users/login.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password", "encodeme")

        if len(email) == 0 or len(password) == 0:
            return redirect(reverse("users:register"))

        users = Users.objects.filter(email=email)

        if users.exists():
            user = users.first()
            if check_password(password, user.password):

                request.session["user_id"] = user.id

                if user.is_first_login == True:
                    # create the favortiate list for the user
                    usertobooklist = UserToBookList()
                    usertobooklist.user_id = user.id
                    usertobooklist.booklist_title = "favorite"
                    usertobooklist.save()

                    # change is_first_login to false
                    user.is_first_login = False
                    user.save()

                return redirect(reverse("users:mine"))
            else:

                return redirect(reverse("users:login"))
        print("user not exists")
        return redirect(reverse("users:login"))


def register(request):
    if request.method == "GET":

        return render(request, "users/register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if len(username) == 0 or len(email) == 0 or len(password) == 0:
            return redirect(reverse("users:register"))

        password = make_password(password)

        user = Users()
        user.name = username
        user.email = email
        user.password = password

        user.save()

        return redirect(reverse("users:login"))


# for registration: check if a email is already registed
def userverify(request):
    email = request.GET.get("email")

    users = Users.objects.filter(email=email)

    data = {"status": constant.HTTP_OK, "msg": "ok"}
    if users.exists():
        data["status"] = constant.HTTP_USER_EXIST
        data["msg"] = "user already exists"
        return JsonResponse(data=data)
    else:
        return JsonResponse(data=data)

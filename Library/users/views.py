import imp
from re import U
import sys
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from users.models import Users
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password

sys.path.append("../Library")
import constant


# Create your views here.
## The BookList System
def createBookList(request):
    return HttpResponse("create book list")


def getUserBookLists(request):
    return HttpResponse("get all book lists for a user")


def getBookList(request):
    return HttpResponse("get all books for a book List")


def deleteBookList(request):
    return HttpResponse("delete book list")


def addBookToList(request):
    return HttpResponse("add book to booklist")


def deleteBookFromList(request):
    return HttpResponse("delete book from book list")


## The login System
def logout(request):
    user_id = request.session.get("user_id")

    if user_id:
        request.session.flush()

    return redirect(reverse("books:get_authors"))


def mine(request):
    user_id = request.session.get("user_id")

    data = {}
    if user_id:
        user = Users.objects.get(id=user_id)
        data["username"] = user.name
        return render(request, "users/usercenter.html", context=data)

    return redirect(reverse("users:login"))


def login(request):
    if request.method == "GET":
        return render(request, "users/login.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password", "encodeme")
        users = Users.objects.filter(email=email)

        if users.exists():
            user = users.first()
            if check_password(password, user.password):
                request.session["user_id"] = user.id
                return redirect(reverse("users:mine"))
            else:
                return redirect(reverse("users:login"))

        return redirect(reverse("users:login"))


def register(request):
    if request.method == "GET":

        return render(request, "users/register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        password = make_password(password)

        user = Users()
        user.name = username
        user.email = email
        user.password = password

        user.save()

        return redirect(reverse("users:login"))


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

import imp
from multiprocessing import context
from re import U
import sys
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from books.models import Book
from users.models import Users, UserToBookList, BookList, Cart
from django.urls import reverse, resolve
from django.contrib.auth.hashers import make_password, check_password
from django.core import serializers


sys.path.append("../Library")
import constant


# Create your views here.

## Shopping cart
def getshoppingcart(request):
    user = request.user

    cart_items = Cart.objects.filter(c_user=request.user)

    data = {"cart_items": cart_items, "username": user.name}
    print(data)
    return render(request, "users/shoppingcart.html", context=data)


def addBookToCart(request):
    # thanks to the middle ware i created, below code are executed iff a user is logged in
    book_tag = request.GET.get("book_tag")
    carts = Cart.objects.filter(c_user=request.user, c_books_tag=book_tag)
    if carts.exists():
        cart_obj = carts.first()
        cart_obj.c_book_num = cart_obj.c_book_num + 1
    else:
        book = Book.objects.filter(book_tag=book_tag).first()
        cart_obj = Cart()
        cart_obj.c_books_tag = book
        cart_obj.c_user = request.user

    cart_obj.save()
    data = {"status": 200, "msg": "add success", "c_books_num": cart_obj.c_book_num}

    return JsonResponse(data=data)


## The BookList System
def createBookList(request):
    user_id = request.session.get("user_id")
    data = {"status": 403, "msg": "user not logged in "}
    if user_id:

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
    user_id = request.session.get("user_id")
    data = {"status": 403, "msg": "user not logged in "}
    if user_id:
        userbooklist = UserToBookList.objects.filter(user_id=user_id).values()

        # userbooklist_json = serializers.serialize("json", userbooklist)
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


def mine(request):
    user_id = request.session.get("user_id")

    data = {}
    if user_id:
        user = Users.objects.get(id=user_id)
        userbooklists = UserToBookList.objects.filter(user_id=user_id).values()

        data["username"] = user.name
        data["booklists"] = userbooklists

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

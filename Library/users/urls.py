from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    ## user login system
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("userverify/", views.userverify, name="userverify"),
    path("mine/", views.mine, name="mine"),
    path("logout/", views.logout, name="logout"),
    ## booklist system
    path("createBookList/", views.createBookList, name="createbooklist"),
    path("getUserBookLists/", views.getUserBookLists, name="getUserBookLists"),
    path("getBookList/", views.getBookList, name="getBookList"),
    path("deleteBookList/", views.deleteBookList, name="deleteBookList"),
    path("addBookToList/", views.addBookToList, name="addBookToList"),
    path("deleteBookFromList/", views.deleteBookFromList, name="deleteBookFromList"),
]

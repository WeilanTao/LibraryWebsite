from django.urls import path 
from . import views

app_name = 'users'
urlpatterns = [
    path("login/", views.login, name = "login"),
    path("register/", views.register, name ="register"),
    path("userverify/", views.userverify, name = "userverify"),
    path("mine/", views.mine, name = "mine")
]
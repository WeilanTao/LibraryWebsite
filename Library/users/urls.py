from django.urls import path 
from . import views

app_name = 'users'
urlpatterns = [
    path("login/", views.login, name = "user_login"),
    path("register/", views.register, name ="user_register")
]
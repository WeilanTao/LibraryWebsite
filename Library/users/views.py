import imp
import sys
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from users.models import Users
from django.urls import reverse
from django.contrib.auth.hashers import make_password

sys.path.append('../Library')
import constant


# Create your views here.
def login(request):
    if request.method =="GET":
        return render(request, "users/login.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password","encodeme")


    return HttpResponse("Login")


def register(request): 
    if request.method == "GET":

        return render(request, "users/register.html")
    elif request.method== "POST":
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

    users = Users.objects.filter(email = email)

    data = {
        "status": constant.HTTP_OK, 
        "msg": "ok"
    }
    if users.exists():
        data['status']=constant.HTTP_USER_EXIST
        data['msg']='user already exists'
        return JsonResponse(data=data)
    else:
        return JsonResponse(data=data)
from django.http import HttpResponse
from django.shortcuts import render
from users.models import Users

# Create your views here.
def login(request):

    return HttpResponse("Login")


def register(request): 
    if request.method == "GET":
        data ={
            "title":"Register"
        }
        return render(request, "users/register.html", context = data)
    elif request.method== "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Users()
        user.name = username
        user.email = email
        user.password = password

        user.save()

        return HttpResponse("REGISTER SUCCESS")
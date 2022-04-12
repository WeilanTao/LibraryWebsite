from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def login(request):

    return HttpResponse("Login")


def register(request): 
    return HttpResponse("register")
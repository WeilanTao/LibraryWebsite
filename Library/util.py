import hashlib
from django.shortcuts import render
from django.template import RequestContext


def hash_str(source):
    return hashlib.new("sha512", source.encode("utf-8")).hexdigest()


def handler404(request):
    print("I am rendering 404 page")
    response = render(request, "404.html")
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response

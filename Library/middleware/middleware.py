from django.utils.deprecation import MiddlewareMixin
from users.models import Users
from django.shortcuts import render, redirect
from django.urls import reverse, resolve

REQUIRE_LIOGIN = [
    "/users/addBookToCart/",
]


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):

        if request.path in REQUIRE_LIOGIN:

            user_id = request.session.get("user_id")

            if user_id:
                try:
                    user = Users.object.get(user_id=user_id)
                    request.user = user
                except:
                    return redirect(reverse("users:login"))

            else:
                return redirect(reverse("users:login"))

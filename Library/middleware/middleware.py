from django.utils.deprecation import MiddlewareMixin
from users.models import Users
from django.shortcuts import render, redirect
from django.urls import reverse, resolve
from django.http import HttpResponse, JsonResponse
import constant

REQUIRE_LIOGIN_JSON = ["/users/createBookList/"]
REQUIRE_LIOGIN = []


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):

        if request.path in REQUIRE_LIOGIN_JSON:

            user_id = request.session.get("user_id")

            if user_id:
                try:
                    user = Users.objects.get(id=user_id)
                    request.user = user
                except:
                    data = {
                        "status": constant.HTTP_REDIRECT,
                        "msg": "user not available",
                    }

                    return JsonResponse(data=data)

            else:
                data = {"status": constant.HTTP_REDIRECT, "msg": "user not log in"}
                return JsonResponse(data=data)

        if request.path in REQUIRE_LIOGIN:

            user_id = request.session.get("user_id")

            if user_id:
                try:
                    user = Users.objects.get(id=user_id)
                    request.user = user
                except:
                    data = {
                        "status": constant.HTTP_REDIRECT,
                        "msg": "user not available",
                    }

                    return redirect(reverse("users:login"))

            else:
                data = {"status": constant.HTTP_REDIRECT, "msg": "user not log in"}
                return redirect(reverse("users:login"))

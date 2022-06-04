from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


class AboutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {"user": request.user.username, "version": "3.6"}
        return render(request, "common/index.html", context)
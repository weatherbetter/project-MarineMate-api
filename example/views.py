from django.http import HttpRequest, JsonResponse
from django.shortcuts import render


def index(request: HttpRequest):
    response = {"message": "Hello world"}
    return JsonResponse(response)

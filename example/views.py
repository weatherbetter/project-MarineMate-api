from django.http import HttpRequest, JsonResponse
from django.shortcuts import render


def index(request: HttpRequest):
    response = {"message": "Hi world it is updated!?"}
    return JsonResponse(response)
